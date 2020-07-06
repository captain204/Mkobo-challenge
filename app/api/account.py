from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Account, Transaction



#Create new account
@api.route('/account', methods=['POST'])
def create_account():
    account = Account.to_json(request.json)
    post.user = g.current_user
    db.session.add(account)
    db.session.commit()
    return jsonify(account.to_json()), 201, \
        {'Location': url_for('api.get_account', id=account.id)}




@api.route('/send', methods=['POST'])
def send():
    account = Account.query.filter_by(user_id=id).first()
    if g.current_user == account.user: 
        return forbidden('You cant send money to yourself')
    data = request.get_json()
    balance = account.balance + data.amount
    account.balance = balance
    try:
        account.update()
        response = {'message':'Transfer successfull'}
        return response, HttpStatus.ok_200.value
    except SQLAlchemyError as e:
        db.session.rollback()
        response = {"error":str(e)}
        return response, HttpStatus.bad_request_400.value

        

