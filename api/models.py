from django.db import models

# Create your models here.
class MainCycle(models.Model):
    click_count = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)

    def click(self):
        click_count += click_power

