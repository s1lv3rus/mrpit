import os

import django
from django.conf import settings


# settings.configure(
#     INSTALLED_APPS=[
#         'django.contrib.auth',
#         'django.contrib.contenttypes',
#         'django.contrib.sessions',
#         'easy_thumbnails',
#         'orders',
#         'shop',
#         'coupons',
#         'account',
#     ],
#     DATABASES={
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3'),
#         }
#     }
# )
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'easy_thumbnails',
        'orders',
        'shop',
        'coupons',
        'account',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'u0937287_mrpit',
            'USER': 'u0937287_adminmr',
            'PASSWORD': 'mrpitadmin555556',
            'HOST': 'localhost',
        }
    },
)

django.setup()

from orders.models import Order

order = Order.published.get(id=4746)
orders = Order.published.all()
for i in range(150):
    order.pk = None
    order.save()
    order.delete()

# for ord in orders:
#     ord.delete()