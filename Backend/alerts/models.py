
# Create your models here.
# alerts/models.py

from django.db import models

class Alert(models.Model):
    VIOLATION_CHOICES = [
        ('WEAPON_DETECTED', 'Weapon Detected'),  # The fix from before
        ('NO_HELMET', 'No Helmet Detected'),
        ('NO_VEST', 'No Safety Vest Detected'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    violation_type = models.CharField(max_length=50, choices=VIOLATION_CHOICES)
    camera_id = models.CharField(max_length=100, blank=True, null=True)
    snapshot = models.ImageField(upload_to='snapshots/', blank=True, null=True)
    clip = models.FileField(upload_to='clips/', blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_violation_type_display()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"