import factory

from django.contrib.auth import get_user_model

from receipts.models import ReceiptItem, Receipt


class UserFactory(factory.django.DjangoModelFactory):
    """Generate a user instance."""
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: f'username-{n}')
    email = factory.Sequence(lambda n: f'user{n}@fake.email')

    class Meta:
        model = get_user_model()


class ReceiptFactory(factory.django.DjangoModelFactory):
    """Generate a `Receipt` model instance."""
    seller = factory.Sequence(lambda n: f'Seller {n}')
    buyer = factory.Sequence(lambda n: f'Buyer {n}')
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Receipt


class ReceiptItemFactory(factory.django.DjangoModelFactory):
    """Generate a `ReceiptItem` model instance."""
    receipt = factory.SubFactory(ReceiptFactory)
    service = factory.Faker('text')
    unit = 'unit'
    rate = 2
    quantity = 10

    class Meta:
        model = ReceiptItem
