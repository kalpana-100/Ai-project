from django.db import models

class Product(models.Model):
    owner = models.ForeignKey(
        'users.CustomUser', 
        on_delete=models.CASCADE, 
        related_name='products'
        )
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    description = models.TextField()
    photo = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name

