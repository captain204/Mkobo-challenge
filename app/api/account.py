from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Account, Transaction



#Create new account
@api.route('/account', methods=['POST'])
def create_account():
    account = Account.from_json(request.json)
    post.user = g.current_user
    db.session.add(account)
    db.session.commit()
    return jsonify(account.to_json()), 201, \
        {'Location': url_for('api.get_account', id=account.id)}

