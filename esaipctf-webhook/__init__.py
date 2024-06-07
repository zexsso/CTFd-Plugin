import json
import os
from functools import wraps
import urllib.request
from urllib.parse import urlparse

from flask import Flask, render_template, request

from CTFd.models import Challenges, Solves, Users, Teams, Submissions, db
from CTFd.utils import config as ctfd_config
from CTFd.utils.dates import ctftime
from CTFd.utils.user import get_current_user
from sqlalchemy import func, case

from .utils.scoreboard import get_scoreboard

from .utils.core import check_submission, is_category_complete_for_team

top_flagger_cache = None
top_failer_cache = None

PAGE_CONTENT = """
<div class="jumbotron">
    <div class="container">
        <h1>EsaipCTF Webhook Plugin</h1>
    </div>
</div>
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <form method="GET" id="notifications_form" autocomplete="off">
                <div class="form-group">
                    <b><label for="url">Webhook URL</label></b>
                    <input class="form-control" id="url" name="url" type="url"
                        value="{url}"
                        placeholder="https://localhost:xxxx/xxxx">
                    <small class="form-text text-muted">
                        The URL is used to send information about each
                        challenge solver.
                    </small>
                </div>
                <br />
                <div class="float-right">
                    <input class="btn btn-success text-center" id="_submit"
                        name="_submit" type="submit" value="Save">
                </div>
            </form>
        </div>
    </div>
</div>
"""


def load(app: Flask):
    set_default_plugin_config(app)

    def challenge_attempt_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)

            if not ctftime() or not is_plugin_configured(app):
                return result

            submission = check_submission(result.json)

            if submission == "error":
                return result
            
            challenge = get_challenge_for_request()
            user = get_current_user()
            team = user.team

            if submission == "incorrect":
                user_fail_counter = Submissions.query.filter_by(user_id=user.id, type="incorrect").count()
                response = {
                    "challenge": challenge.name,
                    "category": challenge.category,
                    "team": "" if team is None else team.name,
                    "user": user.name,
                    "top_failer": get_top_failer(user_fail_counter),
                }
                call_webhook(app.config["ESAIP_WEBHOOK_URL"] + "/incorrect", response)

            if submission == "correct":
                num_solves = get_solvers_count_for_challenge(challenge)
                is_category_complete = is_category_complete_for_team(challenge.category, team.id)
                is_special_chall = False

                user_submissions = (
                    db.session.query(
                        Submissions.date,
                        func.count(case([(Submissions.type == "correct", 1)])).label("correct_count"),
                        func.count(case([(Submissions.type == "incorrect", 1)])).label("incorrect_count"),
                    )
                    .filter(Submissions.user_id == user.id)
                    .first()
                )

                solve_time_str = user_submissions.date.strftime("%Y-%m-%d %H:%M:%S")
                user_solves_counter = user_submissions.correct_count
                user_fail_counter = user_submissions.incorrect_count

                response = {
                    "challenge": challenge.name,
                    "category": challenge.category,
                    "team": "" if team is None else team.name,
                    "user_solves": user_solves_counter,
                    "user_fails": user_fail_counter,
                    "user": user.name,
                    "solve_id": num_solves,
                    "solve_time": solve_time_str,
                    "value": challenge.value,
                    "is_category_complete": is_category_complete,
                    "is_special_chall": is_special_chall, 
                    "top_flagger": get_top_flagger(user_solves_counter),
                    "top_failer": get_top_failer(user_fail_counter),
                    "scoreboard": get_scoreboard(),
                }
                call_webhook(app.config["ESAIP_WEBHOOK_URL"], response)

            return result

        return wrapper

    app.view_functions["api.challenges_challenge_attempt"] = challenge_attempt_decorator(
        app.view_functions["api.challenges_challenge_attempt"]
    )

    @app.route("/admin/esaipctf-webhook", methods=["GET"])
    def plugin_page():
        url = request.args.get("url", None)

        if url and validate_url(url):
            app.config["ESAIP_WEBHOOK_URL"] = url
        else:
            url = app.config["ESAIP_WEBHOOK_URL"]

        page_content = PAGE_CONTENT.format(
            url=url,
        )

        return render_template("page.html", content=page_content)


def set_default_plugin_config(app: Flask):
    app.config["ESAIP_WEBHOOK_URL"] = os.environ.get("ESAIP_WEBHOOK_URL", "")


def is_plugin_configured(app: Flask) -> bool:
    return app.config["ESAIP_WEBHOOK_URL"] != ""


def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except Exception:
        return False


def check_submission_for_valid_flag(data: json) -> bool:
    return (
        isinstance(data, dict)
        and data.get("success")
        and isinstance(data.get("data"), dict)
        and data.get("data").get("status") == "correct"
    )


def get_challenge_for_request() -> Challenges:
    if request.content_type != "application/json":
        request_data = request.form
    else:
        request_data = request.get_json()

    challenge_id = request_data.get("challenge_id")
    challenge = Challenges.query.filter_by(id=challenge_id).first_or_404()

    return challenge


def get_solvers_count_for_challenge(challenge: Challenges) -> int:
    solvers = get_solvers_for_challenge(challenge)

    return solvers.count()


def get_solvers_for_challenge(challenge: Challenges) -> Solves:
    team_mode = ctfd_config.is_teams_mode()

    solvers = Solves.query.filter_by(challenge_id=challenge.id)
    if team_mode:
        solvers = solvers.filter(Solves.team.has(hidden=False))
    else:
        solvers = solvers.filter(Solves.user.has(hidden=False))

    return solvers


def get_top_flagger(new_flagger_number):
    global top_flagger_cache
    nb_top_flagger = top_flagger_cache.get("num_flags", None) if top_flagger_cache else None
    if nb_top_flagger and nb_top_flagger >= new_flagger_number:
        return top_flagger_cache

    top_flagger = (
        db.session.query(
            Users.id.label("user_id"),
            Users.name.label("user_name"),
            Teams.name.label("user_team"),
            func.count(Solves.id).label("correct_count"),
        )
        .join(Solves, Solves.user_id == Users.id)
        .outerjoin(Teams, Teams.id == Users.team_id)
        .group_by(Users.id, Teams.name)
        .order_by(func.count(Solves.id).desc())
        .first()
    )

    if top_flagger:
        top_flagger_cache = {
            "user_id": top_flagger.user_id,
            "user_name": top_flagger.user_name,
            "user_team": top_flagger.user_team,
            "correct_count": top_flagger.correct_count,
        }
        return top_flagger_cache
    return None


def get_top_failer(failer_number):
    global top_failer_cache
    nb_top_failer = top_failer_cache.get("incorrect_count", None) if top_failer_cache else None
    if nb_top_failer and nb_top_failer >= failer_number:
        return top_failer_cache

    top_failer = (
        db.session.query(
            Users.id.label("user_id"),
            Users.name.label("user_name"),
            Teams.name.label("user_team"),
            func.count(Submissions.id).label("incorrect_count"),
        )
        .join(Submissions, Submissions.user_id == Users.id)
        .outerjoin(Teams, Teams.id == Users.team_id)
        .filter(Submissions.type == "incorrect")
        .group_by(Users.id, Teams.name)
        .order_by(func.count(Submissions.id).desc())
        .first()
    )

    if top_failer:
        top_failer_cache = {
            "user_id": top_failer.user_id,
            "user_name": top_failer.user_name,
            "user_team": top_failer.user_team,
            "incorrect_count": top_failer.incorrect_count,
        }
        return top_failer_cache
    return None


def call_webhook(url: str, data: dict) -> None:
    headers = {"Content-Type": "application/json"}
    json_data_bytes = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=json_data_bytes, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        print("Webhook response:", response.read().decode())
    except Exception as e:
        print(f"General error: {e}")
