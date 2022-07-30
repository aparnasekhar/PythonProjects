from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_owner")
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=2000)
    image_url =  models.CharField(max_length=200, blank=True)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=64, blank=True)
    watchlist_owner = models.ManyToManyField(User, blank=True, related_name="watchlist_item")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    commented_item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.commenter} : {self.comment}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_by", default=True)
    bid_item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid", default=True)
    bid_price = models.DecimalField(max_digits=6, decimal_places=2, default=True)
    listingid = models.IntegerField(default=True)

    def __str__(self):
        return f"{self.user} is ready to pay ${self.bid_price} for the item : {self.bid_item}"