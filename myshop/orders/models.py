from django.db import models
from products.models import Product

class Order(models.Model):
    first_name = models.CharField(max_length=100, default="Имя")
    last_name = models.CharField(max_length=100, default="Фамилия")
    email = models.EmailField(default="example@example.com")
    address = models.CharField(max_length=250, default="Без адреса")
    postal_code = models.CharField(max_length=20, default="000000")
    city = models.CharField(max_length=100, default="Без города")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Заказ {self.id} от {self.first_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    def get_cost(self):
        return self.price * self.quantity