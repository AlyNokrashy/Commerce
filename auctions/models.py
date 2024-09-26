from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# First Model
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


# Second Model
class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300, blank=True)
    img = models.CharField(max_length=1000, blank=True, null=True)
    starting_bid = models.ForeignKey(
        "Bid",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="starting_bid_item",
    )
    activity = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="items"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="items",
    )
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlistItem")

    def __str__(self):
        return f"{self.title}"


# Third Model
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}' bid {self.bid_amount}"


# Fourth Model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} commented: {self.comment} on {self.item} item"
