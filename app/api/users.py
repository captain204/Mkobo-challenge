from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Account, Transaction


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())




@api.route('/users/<int:id>/account/')
def get_user_account(id):
    account = Account.query.filter_by(user_id=id).first()
    return jsonify(account.to_json())



@api.route('/users/<int:id>/transactions/')
def get_user_transactions(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagenation = user.transactions.order_by(Transaction.timestamp.desc()).paginate(
        page, per_page=current_app.config['MKOBO_TRANSACTIONS_PER_PAGE'],
        error_out=False)
    transactions = pagenation.items
    prev = None
    if pagenation.has_prev:
        prev = url_for('api.get_user_transactions', id=id, page=page-1)
    next = None
    if pagenation.has_next:
        next = url_for('api.get_transaction',page=page+1)
    return jsonify({
        'transactions': [transaction.to_json() for transaction in transactions],
        'prev': prev,
        'next': next,
        'count': pagenation.total
    })




@api.route('/users/')
def get_users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(
        page, per_page=current_app.config['MKOBO_USERS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_users', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_users', page=page+1)
    return jsonify({
        'users': [user.to_json() for user in users],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })



