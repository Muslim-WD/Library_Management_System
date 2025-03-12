from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.PositiveIntegerField(default=1)  # Tracks book stock

    def is_available(self):
        return self.quantity > 0  # Check availability dynamically

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Admin approval
    returned = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class BorrowHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[("Borrowed", "Borrowed"), ("Returned", "Returned")], default="Borrowed")

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"