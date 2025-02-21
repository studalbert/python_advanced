import factory
import factory.fuzzy as fuzzy
import random

from module_29_testing.hw.main.app import db
from module_29_testing.hw.main.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyFunction(
        lambda: random.choice(["example_credit_card", ""])
    )
    car_number = fuzzy.FuzzyText(prefix="Car")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.LazyAttribute(lambda x: random.choice([True, False]))
    count_places = factory.LazyAttribute(lambda x: random.randint(10, 1000))
    count_available_places = factory.LazyAttribute(
        lambda x: random.randint(0, x.count_places)
    )
