from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    
    is_librarian = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)

    def user_type(self):
        if self.is_librarian:
            return "Librarian"
        elif self.is_member:
            return "Member"

    def __str__(self):
        return self.username

    def books_borrowed(self):
        return Books.objects.filter(borrowed_by=self).count()


class Books(models.Model):

    CHOICES = (
        ('Borrow', 'Borrow'),
        ('Return', 'Return')
    )

    name = models.CharField(max_length=50, blank=False, null=False)
    is_borrowed = models.BooleanField(default=False)

    added_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL,related_name='librarian')

    borrowed_by = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.SET_NULL, related_name='borrower')

    def __str__(self):
        return self.name

    def status(self):
        if self.is_borrowed:
            return "Borrowed"
        else:
            return "Available"
