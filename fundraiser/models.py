from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.
class User(AbstractUser):
    pass

def serialize(self):
    return {
        "id" : self.id,
        "username": self.username

    }

class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="campaignowner")
    title = models.CharField(max_length=100)
    description = models.TextField()
    amount_needed = models.DecimalField(max_digits=7, decimal_places=2)
    end_date = models.DateField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)

    def serialize(self):
        return {
            "id": self.id,
            "user" : self.user.username,
            "title" : self.title,
            "description" : self.description,
            "amount_needed" : self.amount_needed,
            "end_date" : self.end_date.strftime('%b. %d, %Y'),
            "category" : self.category
        }


    def __str__(self):
        return f"{self.title}"

class Donation(models.Model):
    donated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donator")
    donated_for = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="fund")
    donation = models.DecimalField(max_digits=7, decimal_places=2)
    fund_id = models.IntegerField(default=True)

    def serialize(self):
        return {
            "id": self.id,
            "donated_by" : self.donated_by.username,
            "donated_for" : self.donated_for.title,
            "donation" : self.donation,
        }

    def __str__(self):
        return f"{self.donated_by} donated {self.donation} for {self.donated_for}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentby")
    commented_on = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.commenter} : {self.comment}"

class Backer(models.Model):
    backer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donated", default=True)
    backed_campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="fundraiser",default=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=True)

    def __str__(self):
        return f"{self.backer}"

class Message(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="msg_sent")
    recipients = models.ForeignKey("User", on_delete=models.PROTECT, related_name="msg_received")
    subject = models.ForeignKey("Campaign", on_delete=models.CASCADE, related_name="subject", blank=True, default=True)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def serialize(self):
        return{
            "id" : self.id,
            "sender" : self.sender.username,
            "recipients": self.recipients.username,
            "subject" : self.subject.title,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%d/%m/%y %H:%M"),
            "read": self.read
        }

    def __str__(self):
        return f"{self.sender} send a message to {self.recipients}"
       