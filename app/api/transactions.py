from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Account, Transaction
from  app.api.http_status import HttpStatus


@api.route('/transactions')
def get_transactions():
    page = request.args.get('page', 1, type=int)
    pagination = Transaction.query.paginate(
        page, per_page=current_app.config['MKOBO_TRANSACTIONS_PER_PAGE'],
        error_out=False)
    transactions = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_transactions', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_transactions', page=page+1)
    return jsonify({
        'transactions': [transaction.to_json() for transaction in transactions],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
