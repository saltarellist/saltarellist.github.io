from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField



class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watch")
    

class Category(models.Model):
    category = CharField(max_length=64, null=True)

    def __str__(self):
        return self.category

class Listing(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=1000)
    start_bid = models.DecimalField(max_digits=12, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True)
    high_bid = models.ForeignKey("Bid", on_delete=models.CASCADE, related_name="winner", null=True)
    img_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=4)
    

    def __str__(self):
        return f"""{self.title}:
        {self.description}
        {self.id}
        CAD${self.high_bid}"""
    

class Bid(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="bid_item")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True)
    bid = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.bid}"

class Comment(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=1000, blank=True, default=" ")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

