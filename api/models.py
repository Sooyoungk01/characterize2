
from django.db import models

# Create your models here.


class Characters(models.Model):
    name = models.CharField(max_length=15)
    id_ch = models.IntegerField()

    def __str__(self):
        return self.name

class Images(models.Model):
    id_ch = models.IntegerField()
    image = models.ImageField(upload_to="images")