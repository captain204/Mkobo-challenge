from flask import jsonify, request, g, current_app, url_for
from .. import db
from . import api
from ..models import User, Account, Transaction
from  app.api.http_status import HttpStatus
from sqlalchemy.exc import SQLAlchemyError

from ..helpers import account,convert





#Create new account
@api.route('/account', methods=['POST'])
def create_account():
    #account = Account.to_json(request.json)
    data = request.get_json()
    account_user = Account.query.filter_by(user_id=g.current_user.id).first()
    response = {'message':'This account already exists'}
    if account_user:
        return response, HttpStatus.bad_request_400.value
    create_account = Account(account_type=data['account_type'],balance=data['balance'],
                             user_id=g.current_user.id,account_number=account())
    try:
        db.session.add(create_account)
        db.session.commit()
        return jsonify(create_account.to_json()),HttpStatus.ok_200.value
    except SQLAlchemyError as e:
        db.session.rollback()
        response = {"error":str(e)}
        return response, HttpStatus.bad_request_400.value



@api.route('/account/send', methods=['POST'])
def send():
    data = request.get_json()
    account_sender = Account.query.filter_by(user_id=g.current_user.id).first()
    response = {'message':'Insufficient funds'}
    #Check balance
    if not account_sender.balance:
        return response, HttpStatus.bad_request_400.value
    sender_balance = account_sender.balance - data['amount']
    account_sender.balance = sender_balance
    #Receiver check 
    account_receiver = Account.query.filter_by(user_id=data['user_id']).first()
    response = {'message':'You cannot transfer money to yourself'}
    if account_sender == account_receiver:
            return response, HttpStatus.bad_request_400.value
    
    #Reconcilling account balance
    balance = account_receiver.balance + data['amount']
    account_receiver.balance = balance
    
    transaction_sender=Transaction(user_id=g.current_user.id, amount=data['amount'],
                              description=data['description'],transaction_type='debit')
    transaction_receiver=Transaction(user_id=data['user_id'], amount=data['amount'],
                              description=data['description'],transaction_type='credit')
    
    try:
        db.session.add(account_sender)
        db.session.add(account_receiver)
        db.session.add(transaction_sender)
        db.session.add(transaction_receiver)
        db.session.commit()
        response = {'message':'Transfer successfull'}
        return response, HttpStatus.ok_200.value
    except SQLAlchemyError as e:
        db.session.rollback()
        response = {"error":str(e)}
        return response, HttpStatus.bad_request_400.value

    #return jsonify(account.balance)
    
    
        

