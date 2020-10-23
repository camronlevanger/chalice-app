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

@app.route('/users/{user_id}/listteams')
def list_user_teams(user_id):
    teams = session.query(UserTeams) \
    .filter(UserTeams.user_id == user_id) \
    .all()
    print(teams)
    data = {}
    for team in teams:
        row = {}
        row["member"] = team.users.email
        row["team"] = team.teams.name
        row["position"] = team.position
        data[team.team_id] = row
    
    json_data = json.dumps(data)
    session.close()

    return json_data

@app.route('/teams/{team_id}/members', methods=['GET'])
def list_team_members(team_id, sort=False):
    users = session.query(UserTeams) \
    .filter(UserTeams.team_id == team_id) \
    .all()
 
    data = {}
    for user in users:
        row = {}
        row["member"] = user.users.email
        row["position"] = user.position
        data[user.user_id] = row
    
    json_data = json.dumps(data)
    session.close()

    return json_data

@app.route('/users/{email}', methods=['POST'])
def create_user(email):
    user = User(email=email)
    session.add(user)
    session.flush()

    data = {}
    data["id"] = user.id
    data["email"] = user.email

    session.commit()
    session.close()
    return data

@app.route('/users/{email}', methods=['PUT'], content_types=['application/json'])
def update_user(email):
    body = app.current_request.json_body
    user = session.query(User) \
    .filter(User.email == email) \
    .one()

    user.email = body["new_email"]
    session.commit()
    session.close()

    return {'user': email}

@app.route('/teams/{team_id}/members', methods=['POST'], content_types=['application/json'])
def team_add_member(team_id):
    body = app.current_request.json_body
    print(body)
    userteam = UserTeams(team_id=team_id, user_id=body["user_id"], position=body["position"])
    session.add(userteam)
    session.commit()
    session.close()
    return {"team": body["team_id"], "user": body["user_id"], "position": body["position"]}
    # find team, user and create association

@app.route('/teams/{team_id}/members', methods=['PUT'], content_types=['application/json'])
def team_update_member(team_id):
    body = app.current_request.json_body
    user = session.query(UserTeams) \
    .filter(UserTeams.team_id == team_id) \
    .filter(UserTeams.user_id == body["user_id"]) \
    .all()

    user.position = body["position"]
    user.active = body["active"]

    session.commit()
    session.close()
    return True

@app.route('/teams/{team_id}/members', methods=['DELETE'], content_types=['application/json'])
def team_delete_member(team_id):
    body = app.current_request.json_body
    user = session.query(UserTeams) \
    .filter(UserTeams.team_id == team_id) \
    .filter(UserTeams.user_id == body["user_id"]) \
    .all()

    user.active = false

    session.commit()
    session.close()
    return True

@app.route('/invite', methods=['POST'], content_types=['application/json'])
def invite():
    body = app.current_request.json_body
    
    # Parse body, send invite link to user

    return True

@app.route('/invite/accept/{team_id}/{email}/{position}', methods=['POST'])
def accept_invite(team_id, email, position):
    user = create_user(email)

    userteam = UserTeams(team_id=team_id, user_id=user["id"], position=position)
    session.add(userteam)
    session.commit()
    session.close()
    
    return {"team": team_id, "user": email, "position": position}
    
@app.route('/')
def index():
    return {'hello': 'world'}
