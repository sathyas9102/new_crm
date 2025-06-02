from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Stage Choices
STAGES = [
    ("New", "New"),
    ("FollowUp1", "FollowUp1"),
    ("FollowUp2", "FollowUp2"),
    ("FollowUp3", "FollowUp3"),
    ("Not Interested", "Not Interested"),
    ("Won", "Won"),
]

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateField(auto_now_add=True)
    stage = models.CharField(max_length=20, choices=STAGES, default="New")
    moved_by_system = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def days_since_created(self):
        return (timezone.now().date() - self.created_at).days

    def __str__(self):
        return f"{self.name} ({self.phone})"

class CallRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Call to {self.customer.name} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)  # e.g., "call", "add", "move"
    timestamp = models.DateTimeField(auto_now_add=True)
    detail = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

