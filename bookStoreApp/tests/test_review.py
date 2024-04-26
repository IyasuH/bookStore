from django.test import TestCase
from ..models import Author, Category, Book, Review
from django.utils import timezone
from django.contrib.auth.models import User

class TestReviewModel(TestCase):
    """
    TestReviewModel - test cases to test Review model
    """
    def setUp(self):
        """
        to create test review
        """
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

        self.test_review = Review.objects.create(
            book = self.test_book,
            user= self.test_user,
            comment = "test comment",
            rating = 5,
        )

    def test_creation(self):
        """
         test the creation of data
        """
        test_review_ = Review.objects.get(pk=self.test_review.pk)
        self.assertEqual(self.test_review, test_review_)
    
    def test_invalid_values(self):
        """
        to validate books values with different invalid values
        """

    def test_field_validations(self):
        """
        test field validations
        """
        test_review_ = Review.objects.get(pk=self.test_review.pk)
        self.assertIsNotNone(test_review_.comment)
        self.assertIsNotNone(test_review_.rating)

    def test_update(self):
        """
        """
        initial_updated_at = self.test_review.updated_at
        self.test_review.comment = "test updated comment"
        self.test_review.save()
        self.assertEqual(self.test_review.comment, "test updated comment")
        self.assertNotEqual(initial_updated_at, self.test_review.updated_at)


    def test_delete(self):
        """
        test the deletion of data using model
        """
        self.test_review.delete()
        
        with self.assertRaises(Exception):
            Review.objects.get(pk=self.test_review.pk)