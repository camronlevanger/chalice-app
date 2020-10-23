from chalice import Chalice


app = Chalice(app_name='chalice-app')
app.debug = True
app.api.cors = True

from base import Session, engine, Base
from models import User, UserTeams, Team
import json 
session = Session()

@app.route('/create_schema')
def create_schema():
    Base.metadata.create_all(engine)

@app.route('/teams/{name}', methods=['POST'])
def create_team(name):
    team = Team(name=name)
    session.add(team)
    session.commit()
    session.close()
    return {"team": name}

@app.route('/teams', methods=['GET'])
def list_all_teams():
    teams = session.query(Team).all()
    session.close()
    data = {}
    for team in teams:
        data[team.id] = team.name
    
    json_data = json.dumps(data)

    return json_data

@app.route('/users', methods=['GET'])
def list_all_users():
    users = session.query(User).all()
    session.close()
    data = {}
    for user in users:
        data[user.id] = user.email
    
    json_data = json.dumps(data)

    return json_data

@app.route('/users/{team_id}')
def list_users(team_id, sort=False):
    if app.current_request.query_params['sort'] == "true":
        sort = True
    users = session.query(UserTeams) \
    .filter(UserTeams.team_id == team_id) \
    .all()
    return users
    #select team, users, position filter by position and active

@app.route('/teams/{user_id}', methods=['GET'])
def get_teams(user_id):
    if app.current_request.query_params['sort'] == "true":
        sort = True
    users = session.query(UserTeams) \
    .filter(UserTeams.user_id == user_id) \
    .all()
    return users
    #select users, teams sort by active, sort

@app.route('/users/{email}', methods=['POST'])
def create_user(email):
    session.add(User(email=email))
    session.commit()
    session.close()
    return {'user': email}

def team_add_member(team_id, user_id, position):
    return True
    # find team, user and create association

def team_update_member(team_id, user_id, position, active):
    return True
    # find user, team update position and active
@app.route('/')
def index():
    return {'hello': 'world'}

session.commit()
session.close()
