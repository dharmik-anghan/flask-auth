from extentions import db
from flask import abort
from models.user import User
from models.user_request import RequestToUser
from models.follower_following import FollowerFollowing
from api.schemas.follower_following_schema import (
    CreateFollowerSchema,
    CreateRequestSchema,
    RequestResponseSchema,
)
from api.helpers.user_helpers import get_user_by_user_id
from api.schemas.user import UserRequestSchema


def delete_request(cancel_req):
    db.session.delete(cancel_req)
    db.session.commit()
    return True

def operation_on_follower_following_count_on_user_table(follower_id, following_id):
    my_following_count = FollowerFollowing.query.filter_by(followed_by=following_id).count()
    user_follower_count = FollowerFollowing.query.filter_by(followed_to=follower_id).count()

    my_profile = get_user_by_user_id(following_id)
    my_profile.following_count = my_following_count
    
    user_profile = get_user_by_user_id(follower_id)
    user_profile.follower_count = user_follower_count

    db.session.commit()

def generate_follow_req(requested_to, my_id):
    requested = RequestToUser.query.filter_by(
        requested_to=requested_to, requested_by=my_id
    ).first()
    if requested:
        return False

    schema = CreateRequestSchema()
    data = {}
    data["requested_to"] = requested_to
    data["requested_by"] = my_id

    try:
        user_data = schema.load(data)
        db.session.add(user_data)
        db.session.commit()
    except Exception as e:
        abort(500, e)
    return True


def start_following(requested_to, my_id):
    
    user = FollowerFollowing.query.filter_by(
        followed_by=my_id, followed_to=requested_to
    ).first()
    if user:
        return False
    schema = CreateFollowerSchema()
    data = {}
    data["followed_to"] = requested_to
    data["followed_by"] = my_id

    user_data = schema.load(data)
    db.session.add(user_data)
    db.session.commit()
    return True


def accept_request(requested_to, my_id):
    
    user = FollowerFollowing.query.filter_by(
        followed_by=requested_to, followed_to=my_id
    ).first()
    if user:
        return False
    schema = CreateFollowerSchema()
    data = {}
    data["followed_to"] = my_id
    data["followed_by"] = requested_to

    user_data = schema.load(data)
    db.session.add(user_data)
    db.session.commit()
    return True
    


def get_request_list(user_id):
    try:
        request_list = RequestToUser.query.filter_by(requested_to=user_id).all()
        if request_list is None:
            return {"msg": "N"}
        schema = RequestResponseSchema(many=True)
        dict_list = schema.dump(request_list)
        users = []
        for idx, req_user in enumerate(dict_list):
            id = req_user.get("requested_by")
            user = get_user_by_user_id(id)
            schema = UserRequestSchema()
            user_dict = schema.dump(user)
            users.append(user_dict)
            users[idx]["requested_at"] = req_user.get("created_at")
        return users
    except Exception as e:
        abort(404, e)

def get_request_from_table(followed_to, user_id):
    req =  RequestToUser.query.filter_by(requested_to=user_id, requested_by=followed_to).first()
    return req

