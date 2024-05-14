from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateField()
    author = models.ForeignKey("Author", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.author} in {self.pub_date}"


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Reader(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=3)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return f"{self.name}"
