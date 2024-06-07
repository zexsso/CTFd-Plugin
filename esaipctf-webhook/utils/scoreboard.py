from collections import defaultdict

from CTFd.models import Awards, Solves
from CTFd.utils.dates import isoformat

from CTFd.utils.scores import get_standings


def get_scoreboard():
    response = {}
    standings = get_standings()

    team_ids = [team.account_id for team in standings]

    solves = Solves.query.filter(Solves.account_id.in_(team_ids))
    awards = Awards.query.filter(Awards.account_id.in_(team_ids))

    solves = solves.all()
    awards = awards.all()

    # Build a mapping of accounts to their solves and awards
    solves_mapper = defaultdict(list)
    for solve in solves:
        solves_mapper[solve.account_id].append(
            {
                "challenge_id": solve.challenge_id,
                "account_id": solve.account_id,
                "team_id": solve.team_id,
                "user_id": solve.user_id,
                "value": solve.challenge.value,
                "date": isoformat(solve.date),
            }
        )

    for award in awards:
        solves_mapper[award.account_id].append(
            {
                "challenge_id": None,
                "account_id": award.account_id,
                "team_id": award.team_id,
                "user_id": award.user_id,
                "value": award.value,
                "date": isoformat(award.date),
            }
        )

    # Sort all solves by date
    for team_id in solves_mapper:
        solves_mapper[team_id] = sorted(solves_mapper[team_id], key=lambda k: k["date"])

    for i, _team in enumerate(team_ids):
        response[i + 1] = {
            "id": standings[i].account_id,
            "name": standings[i].name,
            "solves": solves_mapper.get(standings[i].account_id, []) if i < 10 else [],
            "solves_count": len(solves_mapper.get(standings[i].account_id, [])),
            "score": float(standings[i].score),
        }

    return response
