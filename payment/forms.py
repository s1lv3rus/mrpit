from django import forms


class PaymentCreateForm(forms.Form):
    merchant = forms.CharField(required=True)  # идентификатор магазина
    amount = forms.FloatField(required=True)  # сумма платежа 2 знака после точки
    order_id = forms.IntegerField(required=True)  # id заказа уникальный
    description = forms.Field(required=True)  # описание платежа
    success_url = forms.URLField(required=True) # урл, на который нужно отправить Клиента после удачной оплаты
    testing = forms.BooleanField(required=True, )  # идентификатор для тестирования, должен быть 1, если тестируем
    callback_url = forms.URLField(required=True)  # урл, на который будет отправлено уведомление в случае успешной
    # оплаты.
    callback_on_failure = forms.BooleanField(required=True)  # Включение/отключение отправки уведомления, когда
    # операция завершилась неуспешно. 1 – отправлять; 0 - не отправлять.
    signature = forms.Field(required=True)  # Криптографическая подпись. Алгоритм вычисления вычисления подписи описан
    # в разделе «Алгоритм вычисления поля signature».
