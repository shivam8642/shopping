from django.db import models


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to = 'products', default='')
    description = models.CharField(max_length=100)
    is_featured = models.BooleanField('featured')
    is_new_stock = models.BooleanField('new stock')
    is_sale_available = models.BooleanField('sale')
    
    def __str__(self):
        return self.product_name

class Slider(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    describe = models.CharField(max_length=200)
    image_1 = models.ImageField(upload_to = 'products', default='')

    def __str__(self):
        return self.title


class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    user_id = models.IntegerField()
    created_at = models.DateTimeField()


class Address(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address= models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    mobile_no = models.CharField(max_length=10)
    user_id=models.IntegerField(default='')



    
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    user_id = models.IntegerField()
    created_at = models.DateTimeField()
    stripe_payment_intent = models.CharField(max_length=2000)
    has_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=10)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,default='')