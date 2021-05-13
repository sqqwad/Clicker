from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MainCycle(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)

    def click(self):
        self.click_count += self.click_power
