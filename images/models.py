from django.db import models


# Create your models here.
class Image(models.Model):
    url = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'images'
