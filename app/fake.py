from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User


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



