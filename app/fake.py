from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Account, Transaction




def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 password='password',
                 confirmed=True,
                 firstname=fake.first_name(),
                 lastname=fake.last_name(),
                 location=fake.city(),
                 registered_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def accounts(count=6):
    fake= Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        account = Account(account_type='savings',
                          balance=0,
                          user=u)
        db.session.add(account)
    db.session.commit()


def transactions(count=6):
    fake= Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        transaction = Transaction(amount=1000,
                          description=fake.sentence(),
                          transaction_type='credit',
                          user=u)
        db.session.add(transaction)
    db.session.commit()

    