from extentions import db
from flask import request, abort
from flask_restful import Resource
from models.user_request import RequestToUser
from models.follower_following import FollowerFollowing
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.helpers.user_helpers import (
    check_user_email_verification,
    get_user_by_user_id,
    check_user_account_status,
)
from api.helpers.follow_req_helpers import (
    generate_follow_req,
    start_following,
    delete_request,
    get_request_list,
    get_request_from_table,
    operation_on_follower_following_count_on_user_table,
    accept_request
)


class FollowerResource(Resource):
    method_decorators = [jwt_required()]

    @check_user_email_verification
    @check_user_account_status
    def get(self):
        user_id = get_jwt_identity()
        user = get_user_by_user_id(user_id)

        if request.path == "/user/get-req-user-list" and user.is_public is not True:
            list_of_req = get_request_list(user_id)
            return {"requests": list_of_req}
        else:
            return {"msg": "Page not found"}, 404

    @check_user_email_verification
    @check_user_account_status
    def post(self):
        followed_to = request.args.get("followed_to", type=int)
        if not followed_to:
            return {"msg": "Missing user id in params"}

        user_id = get_jwt_identity()
        if user_id == followed_to:
            return {"msg": "Can't process request"}
        my_profile = get_user_by_user_id(user_id)

        user = get_user_by_user_id(followed_to)
        username = user.username

        if request.path == "/user/accept-request":
            if  my_profile.is_public is True:
                return {"msg": "Page not found"}, 404
            req = get_request_from_table(followed_to, user_id)
            if req:
                followed = accept_request(followed_to, user_id)
                if followed:
                    db.session.delete(req)
                    db.session.commit()
                    operation_on_follower_following_count_on_user_table(user_id, followed_to)
                    return {"msg": f"{username} started following you"}
                else:
                    return {"msg": f"{username} already following"}
            else:
                return {"msg": "No request found"}
        
        try:
            if user.is_public:
                followed = start_following(followed_to, user_id)
                if followed:
                    operation_on_follower_following_count_on_user_table(followed_to, user_id)
                    return {"msg": f"started following {username}"}
                else:
                    return {"msg": f"User alreay following {username}"}
            else:
                generated_req = generate_follow_req(followed_to, user_id)
                if generated_req:
                    username = user.username
                    return {"msg": f"Request sent to {username}"}
                else:
                    return {"msg": f"Request already sent to {username}"}
        except Exception as e:
            abort(404, e)

    @check_user_email_verification
    @check_user_account_status
    def delete(self):
        requested_to = request.args.get("requested_to", type=int)

        if not requested_to:
            return {"msg": "Missing user id in params"}

        user_id = get_jwt_identity()
        if user_id == requested_to:
            abort(404)

        user = get_user_by_user_id(requested_to)

        try:
            unfollow = FollowerFollowing.query.filter_by(
                followed_to=requested_to
            ).first()
            cancel_req = RequestToUser.query.filter_by(
                requested_to=requested_to
            ).first()
            if unfollow:
                db.session.delete(unfollow)
                db.session.commit()
                operation_on_follower_following_count_on_user_table(requested_to, user_id)
                username = user.username
                return {"msg": f"Unfollowed {username}"}
            elif cancel_req:
                req_deleted = delete_request(cancel_req)
                if req_deleted:
                    username = user.username
                    return {"msg": f"Follow request cancelled to {username}"}
                else:
                    return {"msg": "Something went wrong"}, 500
            else:
                return {"msg": "You are not follwing person"}
        except Exception as e:
            abort(404, e)
