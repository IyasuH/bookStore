from django.test import TestCase
from ..models import Author, Category, Book
from django.utils import timezone

class TestBookModel(TestCase):
    """
    TestBookModel - test cases to test Book Model
    """
    def setUp(self):
        self.test_author = Author.objects.create(
            full_name = "test author",
            dob=timezone.now(),
            bio="test bio",
        )
        self.test_category= Category.objects.create(
            name="test category"
        )
        self.test_book = Book.objects.create(
            title="Test book",
            author=self.test_author,
            description="test description",
            price=100.00)

        self.test_book.categories.set([self.test_category])
    def test_creation(self):
        """
         tests if the data exists
        """
        test_book_ = Book.objects.get(pk=self.test_book.pk)
        self.assertEqual(self.test_book, test_book_)

    def test_get_invalid_id(self):
        """
         tests to get book object using unavailable/invalid ids
        """
        with self.assertRaises(Exception):
            Book.objects.get(pk=0).delete()
            Book.objects.get(pk="").delete()

    def test_invalid_values(self):
        """
         to validate books values with different invalid values
           - long title, more than defined on model
           - string price, where price defined in the model was as decimal values
           - with only book title, where othere required fields are not filled
           - empty, book with no values
        """
        book_with_long_ttile = Book(
            title="Test book"*100,
            author=self.test_author,
            description="test description",
            price=100.00
        )
        with self.assertRaises(Exception):
            book_with_long_ttile.full_clean()

        book_with_str_price = Book(
            title="Test book",
            author=self.test_author,
            description="test description",
            price=""
        )

        with self.assertRaises(Exception):
            book_with_str_price.full_clean()

        only_title_book = Book(title="test title")

        with self.assertRaises(Exception):
            only_title_book.full_clean()

        empty_book = Book()

        with self.assertRaises(Exception):
            empty_book.full_clean()

    def test_fields_validations(self):
        """
        to test the fields writen on db are not null
        """
        test_book_ = Book.objects.get(pk=self.test_book.pk)
        self.assertIsNotNone(test_book_.title)
        self.assertIsNotNone(test_book_.author)
        self.assertIsNotNone(test_book_.description)
        self.assertIsNotNone(test_book_.price)
        self.assertIsNotNone(test_book_.categories)

    def test_update(self):
        """
        to test update data using the model
         - > that update time will change
         - > also to test the update field
        """
        initial_updated_at = self.test_book.updated_at
        self.test_book.title = "test updated title"
        self.test_book.save()
        self.assertEqual(self.test_book.title, "test updated title")
        self.assertNotEqual(initial_updated_at, self.test_book.updated_at)

    def test_delete(self):
        """
        test the deletion of data using model
        """
        self.test_book.delete()
        
        with self.assertRaises(Exception):
            Book.objects.get(pk=self.test_book.pk)