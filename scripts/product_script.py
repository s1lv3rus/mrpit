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

from shop.models import Product

products = Product.published.all()
for product in products:
    flavours = product.flavours_by_product()
    if flavours.count() == 0:
        with open('log_script.txt', 'a') as outFile:
            outFile.write('{}{}'.format(product.name, product.supplier))

