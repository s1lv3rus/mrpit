from orders.models import Order

for i in range(0, 10000):
    order = Order.published.create()
    i += 1
