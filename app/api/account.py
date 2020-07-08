from flask import jsonify, request, g, current_app, url_for
from .. import db
from . import api
from ..models import User, Account, Transaction
from  app.api.http_status import HttpStatus





#Create new account
@api.route('/account', methods=['POST'])
def create_account():
    account = Account.to_json(request.json)
    account.user = g.current_user
    db.session.add(account)
    db.session.commit()
    return jsonify(account.to_json()), 201, \
        {'Location': url_for('api.get_account', id=account.id)}




@api.route('/account/send', methods=['POST'])
def send():
    data = request.get_json()
    account = Account.query.filter_by(user_id=data['user_id']).first()
    balance = account.balance + data['amount']
    account.balance = balance    
    transaction=Transaction(user_id=g.current_user, amount=data['amount'],
                              description=data['description'],transaction_type='debit')
    db.session.add(account)
    db.session.add(transaction)
    db.session.commit()
    response = {'message':'Transfer successfull'}
    return response, HttpStatus.ok_200.value
    #return jsonify(account.balance)
    
    
        

