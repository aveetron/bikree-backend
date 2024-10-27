from django.db import models

from core.base_abstract_models import BikreeBaseModel


class Order(BikreeBaseModel):
	total = models.DecimalField(max_digits=20, decimal_places=3, default=0.00)
	customer = models.ForeignKey("shop.Customer", on_delete=models.CASCADE)
	is_paid = models.BooleanField(default=False)
	total_payable = models.DecimalField(max_digits=20, decimal_places=3, default=0.00)
	remarks = models.TextField(null=True, blank=True)
	status = models.BooleanField(default=False)  

	def __str__(self):
		return f"Order {self.id}"
	

class OrderDetail(BikreeBaseModel):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	inventory = models.ForeignKey("shop.Inventory", on_delete=models.CASCADE)
	qty = models.DecimalField(max_digits=20, decimal_places=3, default=0.00)
	price = models.DecimalField(max_digits=20, decimal_places=3, default=0.00)
	remarks = models.TextField(null=True, blank=True)

	def __str__(self):
		return f"Order {self.order.id} Inventory {self.inventory.name}"