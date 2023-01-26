from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    customer = models.ForeignKey(Customer, related_name="products", on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    total = models.IntegerField() 

    def __str__(self):
        return self.description