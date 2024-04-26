from django.test import TestCase
from ..models import Author, Category, Book, Order
from django.utils import timezone
from django.contrib.auth.models import User

class TestOrderModel(TestCase):
    """
    """
    def setUp(self):
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
    def test_creation(self):
        """
            test the creation of order
        """
        test_order_ = Order.objects.get(pk=self.test_order.pk)
        self.assertEqual(self.test_order, test_order_)

    def test_field_validations(self):
        """
        test field validations
        """
        test_order_ = Order.objects.get(pk=self.test_order.pk)
        self.assertIsNotNone(test_order_.user)
        self.assertIsNotNone(test_order_.book)
        
    def test_update(self):
        """
        """
        initial_updated_at = self.test_order.updated_at
        self.test_order.country = "test updated country"
        self.test_order.save()
        self.assertEqual(self.test_order.country, "test updated country")
        self.assertNotEqual(initial_updated_at, self.test_order.updated_at)

    def test_delete(self):
        """
        test the deletion of data using model
        """
        self.test_order.delete()
        with self.assertRaises(Exception):
            Order.objects.get(pk=self.test_order.pk)