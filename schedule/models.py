# Your Event model in models.py
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Event Title")
    start = models.DateTimeField(verbose_name="Start Time")
    end = models.DateTimeField(null=True, blank=True, verbose_name="End Time")
    description = models.TextField(null=True, blank=True, verbose_name="Event Description")
    resourceId = models.CharField(max_length=100, choices=[('a', 'Room A'), ('b', 'Room B')], verbose_name="Room")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ["start"]
