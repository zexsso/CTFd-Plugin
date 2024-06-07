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
from sqlalchemy import func, case, and_


def check_submission(data: json) -> str:
    if data.get('success'):
        if 'status' in data.get('data', {}):
            return data['data']['status']
        else:
            return "error"
    else:
        return "error"
    

def is_category_complete_for_team(category, team_id):
    total_challenges_in_category = db.session.query(func.count(Challenges.id)).filter_by(category=category).scalar()
    challenges_solved_by_team = db.session.query(func.count(Solves.challenge_id)).join(Challenges).filter(
        and_(
            Challenges.category == category,
            Solves.team_id == team_id
        )
    ).scalar()
    
    # Comparer les deux
    return total_challenges_in_category == challenges_solved_by_team