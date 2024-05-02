from django.db import models

# Create your models here.
class Task(models.Model):
    content = models.CharField(max_length=255, null=False)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    PRIOR_RANK_CHOICES = [
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low'),
    ]
    prior_rank = models.IntegerField(
        choices=PRIOR_RANK_CHOICES,
        default=2,
    )

    def __str__(self):
        return self.content
        