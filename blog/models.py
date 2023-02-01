from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):  # CREATE TABLE IF NOT EXISTS category
    # title VARCHAR(30) UNIQUE
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title


class Article(models.Model):  # CREATE TABLE IF NOT EXISTS article
    # title VARCHAR(255) UNIQUE
    title = models.CharField(max_length=255, unique=True)
    # content TEXT
    content = models.TextField()
    # photo
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    # created_at
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at
    updated_at = models.DateTimeField(auto_now=True)
    # views INTEGER
    views = models.IntegerField(default=0)
    # publish BOOLEAN DEFAULT TRUE
    publish = models.BooleanField(default=True)
    # category FOREIGN KEY(category_id) REFERENCES category(category_id)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # from django.urls import reverse

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_id': self.pk})

    def __str__(self):
        return self.title

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return "https://www.peerspace.com/resources/wp-content/uploads/2019/02/beverage-3157395_1280.jpg"
