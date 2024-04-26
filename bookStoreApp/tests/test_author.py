from django.test import TestCase
from ..models import Author, Category, Book
from django.utils import timezone

class TestAuthorModel(TestCase):
    """
    AuthorModelTest - test cases to test Author Model
    """
    def setUp(self):
        self.test_author = Author.objects.create(
            full_name = "test author",
            dob=timezone.now(),
            bio="test bio",
        )
    def test_creation(self):
        """
         tests if the data exists
        """
        test_author_ = Author.objects.get(pk=self.test_author.pk)
        self.assertEqual(self.test_author, test_author_)

    def test_invalid_values(self):
        """
         to validate authors values with different invalid values
           - long full_name, more than defined on model
           - string dob, where price defined in the model was as decimal values
           - with only book full_name, where othere required fields are not filled
           - empty, author with no values
        """
        author_with_long_name = Author(
            full_name = "test author" * 100,
            dob=timezone.now(),
            bio = "test bio"
        )

        with self.assertRaises(Exception):
            author_with_long_name.full_clean()

        author_with_str_dob = Author(
            full_name = "test full name",
            dob = "string date",
            bio = "test bio"
        )

        with self.assertRaises(Exception):
            author_with_str_dob.full_clean()

        author_with_full_name = Author(
            full_name = "test full name"
        )

        with self.assertRaises(Exception):
            author_with_full_name.full_clean()

        empty_author = Author() 

        with self.assertRaises(Exception):
            empty_author.full_clean()

    def test_fields_validations(self):
        """
        to test the fields writen on db are not null
        """
        test_author_ = Author.objects.get(pk=self.test_author.pk)
        self.assertIsNotNone(test_author_.full_name)
        self.assertIsNotNone(test_author_.dob)
        self.assertIsNotNone(test_author_.bio)

    def test_update(self):
        """
        to test update data using the model
         - > that update time will change
         - > also to test the update field
        """
        initial_updated_at = self.test_author.updated_at
        self.test_author.full_name = "test updated author name"
        self.test_author.save()
        self.assertEqual(self.test_author.full_name, "test updated author name")
        self.assertNotEqual(initial_updated_at, self.test_author.updated_at)

    def test_delete(self):
        """
        test the deletion of data using model
        """
        self.test_author.delete()
        with self.assertRaises(Exception):
            Book.objects.get(pk=self.test_author.pk)
