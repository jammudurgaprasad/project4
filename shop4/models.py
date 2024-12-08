from django.db import models
from django.contrib.auth.models import User


class Biryani(models.Model):
    CATEGORY_CHOICES = [
        ('biryani', 'Biryani'),
        ('veg_starters', 'Veg Starters'),
        ('nonveg_starters', 'Non-Veg Starters'),
        ('veg_curries', 'Veg Curries'),
        ('nonveg_curries', 'Non-Veg Curries'),
        ('fried_rice', 'Fried Rice'),
        ('tandoori', 'Tandoori'),
    ]
    
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='img')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    @property
    def final_price(self):
        return self.price - ((self.price / 100) * self.discount)

    def __str__(self):
        return f"{self.name}, {self.price}"


class Addresses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    fullname = models.CharField(max_length=40)
    phone = models.IntegerField()
    pincode = models.CharField(max_length=6)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    doorno = models.CharField(max_length=100)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.state}, {self.city}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    biryani = models.ForeignKey(Biryani, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



    def __str__(self):
        return f"{self.biryani.name} (x{self.quantity})"

    @property
    def total_price(self):
        return self.biryani.final_price * self.quantity



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    biryani = models.ForeignKey(Biryani, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")  # "Pending", "Cancelled"
    order_date = models.DateTimeField(auto_now_add=True)

    address = models.ForeignKey(Addresses, on_delete=models.CASCADE, related_name='orders', default=None, null=True)


    def __str__(self):
        return f"Order {self.id}: {self.biryani.name} (x{self.quantity})"
    

