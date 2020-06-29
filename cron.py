import datetime

# import schedule

import django
from django.conf import settings
from django.core.mail import send_mail

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'easy_thumbnails',
        'shop',
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
    DEBUG=True,
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    EMAIL_HOST='smtp.mrpit.online',
    USERNAME='no-repeat@mrpit.online',
    PASSWORD='adminmrpitS555556',
    EMAIL_PORT=587,
    DEFAULT_FROM_EMAIL='no-repeat@mrpit.online',
)

# settings.configure(
#     INSTALLED_APPS=[
#         'django.contrib.auth',
#         'django.contrib.contenttypes',
#         'django.contrib.sessions',
#         'easy_thumbnails',
#         'shop',
#     ],
#     DATABASES={
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'u0937287_mrpit',
#             'USER': 'u0937287_adminmr',
#             'PASSWORD': 'mrpitadmin555556',
#             'HOST': 'localhost',
#         }
#     }
#     ,
#     DEBUG=False,
#     EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
# )

django.setup()


from shop.models import Subscribe

subscribes = Subscribe.published.all()
for sub in subscribes:
    product = sub.product
    flavours = product.flavours_by_product()
    i = 0
    flavours_list = []
    for flavour in flavours:
        if flavour.quantity > 0:
            i += flavour.quantity
            flavours_list.append(flavour.name)
    if i > 0:
        name = 'Mrpit.online'
        email_from = 'no-repeat@mrpit.online'
        email_to = sub.email
        message = 'Товар "{}" поступил на склад.\n' \
                  'В наличии доступны следующие вкусы: \n' \
                  '{}\n' \
                  'Заказывайте прямо сейчас по ссылке https://mrpit.online/product/{}\n\n' \
                  'С уважением, Администрация Интернет-магазина Mrpit.online'.format(product.name, flavours_list,
                                                                                     product.slug)
        send_mail(name, message, email_from, [email_to])

        with open('log_subscribe.txt', 'a') as outFile:
            outFile.write('\nОтправка на {}, время отправки:{}, товар: {}'.format(email_to,
                                                                                  datetime.datetime.now(),
                                                                                  product))
        sub.delete()


# schedule.every(5).seconds.do(job)
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)
