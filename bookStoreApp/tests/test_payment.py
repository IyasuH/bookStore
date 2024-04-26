from django.test import TestCase
from ..models import Author, Category, Book, Payment, Order
from django.utils import timezone
from django.contrib.auth.models import User

class TestPaymentModel(TestCase):
    """
    TestPaymentModel - test cases to test Review model
    """
    def setUp(self):
        """
        to create test review
        """
        # order, stripe_id, status, amount, currency_conersion_rate, payemnt_method
        self.test_user = User.objects.create_user(username="test user", password="test password")
        self.test_author = Author.objects.create(
            full_name = "test author",
            dob=timezone.now(),
            bio="test bio",
        )
        self.test_category= Category.objects.create(name="test category")
        self.test_author = Author.objects.create(
            full_name = "test author",
            dob=timezone.now(),
            bio="test bio",
        )
        self.test_book = Book.objects.create(
            title="Test book",
            author=self.test_author,
            description="test description",
            price=100.00)
        self.test_book.categories.set([self.test_category])
        self.test_order = Order.objects.create(
            user=self.test_user,
            book=self.test_book)

        self.test_payment = Payment(
            order=self.test_order,
            stripe_transaction_id="123abcXYZ",
            status="pending",
            amount=100.00,
            currency_conversion_rate=1.0000,
            payment_method="debit card"
        )

    def test_creation(self):
        """
         test the creation of data
        """
        test_payment_ = Payment.objects.get(pk=self.test_payment.pk)
        self.assertEqual(self.test_payment, test_payment_)
    
    def test_invalid_values(self):
        """
        to validate books values with different invalid values
        """

    def test_field_validations(self):
        """
        test field validations
        """
        test_payment_ = Payment.objects.get(pk=self.test_payment.pk)
        self.assertIsNotNone(test_payment_.stripe_transaction_id)
        self.assertIsNotNone(test_payment_.status)
        self.assertIsNotNone(test_payment_.amount)
        self.assertIsNotNone(test_payment_.currency_conversion_rate)
        self.assertIsNotNone(test_payment_.payment_method)

    def test_update(self):
        """
        """
        initial_updated_at = self.test_payment.updated_at
        self.test_payment.stripe_transaction_id = "updated transaction"
        self.test_payment.save()
        self.assertEqual(self.test_payment.stripe_transaction_id, "updated transaction")
        self.assertNotEqual(initial_updated_at, self.test_payment.updated_at)

    def test_delete(self):
        """
        test the deletion of data using model
        """
        self.test_payment.delete()

        with self.assertRaises(Exception):
            Payment.objects.get(pk=self.test_payment.pk)