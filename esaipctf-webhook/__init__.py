import json
import os
from functools import wraps
import urllib.request
from urllib.parse import urlparse

from flask import Flask, render_template, request

from CTFd.models import Challenges, Solves, Teams, Submissions
from CTFd.utils import config as ctfd_config
from CTFd.utils.dates import ctftime
from CTFd.utils.user import get_current_team, get_current_user

from .plugin_api.scoreboard import get_scoreboard

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

            if check_submission_for_valid_flag(result.json):
                challenge = get_challenge_for_request()
                num_solves = get_solvers_count_for_challenge(challenge)

                user = get_current_user()
                team = get_current_team()

                solve_time = Submissions.query.filter_by(challenge_id=challenge.id, user_id=user.id).first().date
                solve_time_str = solve_time.strftime('%Y-%m-%d %H:%M:%S')

                response = {
                    "challenge": challenge.name,
                    "category": challenge.category,
                    "team": "" if team is None else team.name,
                    "user": user.name,
                    "solve_id": num_solves,
                    "solve_time": solve_time_str,
                    "value": challenge.value,
                    "scoreboard": get_scoreboard(),
                }
                call_webhook(app.config["SOLVE_WEBHOOK_URL"], response)

            return result

        return wrapper

    app.view_functions["api.challenges_challenge_attempt"] = challenge_attempt_decorator(
        app.view_functions["api.challenges_challenge_attempt"]
    )

    @app.route("/admin/esaipctf-webhook", methods=["GET"])
    def plugin_page():
        url = request.args.get("url", None)

        if url and validate_url(url) :
            app.config["SOLVE_WEBHOOK_URL"] = url
        else:
            url = app.config["SOLVE_WEBHOOK_URL"]

        page_content = PAGE_CONTENT.format(
            url=url,
        )

        return render_template("page.html", content=page_content)


def set_default_plugin_config(app: Flask):
    app.config["SOLVE_WEBHOOK_URL"] = os.environ.get("SOLVE_WEBHOOK_URL", "")


def is_plugin_configured(app: Flask) -> bool:
    return app.config["SOLVE_WEBHOOK_URL"] != ""


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


def call_webhook(url: str, data: dict) -> None:
    headers = {"Content-Type": "application/json"}
    json_data_bytes = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=json_data_bytes, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        print("Webhook response:", response.read().decode())
    except Exception as e:
        print(f"General error: {e}")