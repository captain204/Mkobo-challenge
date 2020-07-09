from flask import jsonify, request, g, current_app, url_for
from .. import db
from . import api
from ..models import User, Account, Transaction
from  app.api.http_status import HttpStatus
from sqlalchemy.exc import SQLAlchemyError






#Create new account
@api.route('/account', methods=['POST'])
def create_account():
    account = Account.to_json(request.json)
    account.user_id = g.current_user
    db.session.add(account)
    db.session.commit()
    return jsonify(account.to_json()), 201, \
        {'Location': url_for('api.get_account', id=account.id)}




@api.route('/account/send', methods=['POST'])
def send():
    data = request.get_json()
    account_sender = Account.query.filter_by(user_id=g.current_user.id).first()
    response = {'message':'Insufficient funds'}
    if not account_sender.balance:
        return response, HttpStatus.bad_request_400.value
    sender_balance = account_sender.balance - data['amount']
    account_sender.balance = sender_balance 
    account_receiver = Account.query.filter_by(user_id=data['user_id']).first()
    balance = account_receiver.balance + data['amount']
    account_receiver.balance = balance    
    transaction_sender=Transaction(user_id=g.current_user.id, amount=data['amount'],
                              description=data['description'],transaction_type='debit')
    transaction_receiver=Transaction(user_id=data['user_id'], amount=data['amount'],
                              description=data['description'],transaction_type='credit')
    
    db.session.add(account_sender)
    db.session.add(account_receiver)
    db.session.add(transaction_sender)
    db.session.add(transaction_receiver)
    db.session.commit()
    response = {'message':'Transfer successfull'}
    return response, HttpStatus.ok_200.value
    #return jsonify(account.balance)
    
    
        

