from django.db import models

from django.db.models import CASCADE

from finance.queryset.transaction import TransactionQuerySet
from finance.queryset.transaction_payme import TransactionPaymeQuerySet


class Transaction(models.Model):
    WAITING = 1
    SUCCESS = 2
    CANCEL = -1
    CANCELED_AFTER_CLOSE = -2

    STATUS = (
        (WAITING, 'Ожидание'),
        (SUCCESS, 'Успешно'),
        (CANCEL, 'Отменен'),
        (CANCELED_AFTER_CLOSE, 'Отменен после завершения'),
    )

    CASH = 'cash'
    CARD = 'card'

    TYPE = (
        (CASH, 'Наличие'),
        (CARD, 'Онлайн')
    )

    amount = models.BigIntegerField()
    description = models.TextField()
    order = models.OneToOneField('blog.Order', CASCADE, related_name='transaction')
    state = models.CharField(max_length=255, choices=STATUS, default=WAITING)
    type = models.CharField(max_length=255, choices=TYPE, default=CARD)

    objects = TransactionQuerySet.as_manager()

    class Meta:
        db_table = 'finance_transactions'
        default_related_name = 'transactions'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        unique_together = ('order',)


class TransactionPayme(models.Model):
    WAITING = 1
    SUCCESS = 2
    CANCEL = -1
    CANCELED_AFTER_CLOSE = -2

    TYPE = (
        (WAITING, 'Ожидание'),
        (SUCCESS, 'Успешно'),
        (CANCEL, 'Отменен'),
        (CANCELED_AFTER_CLOSE, 'Отменен после завершения'),
    )
    trans_id = models.CharField(max_length=255, editable=False)
    perform_time = models.DateTimeField(null=True, blank=True)
    cancel_time = models.DateTimeField(null=True, blank=True)
    amount = models.CharField(max_length=255)
    time = models.DateTimeField()
    state = models.CharField(max_length=255, choices=TYPE, default=WAITING)
    last_method = models.CharField(max_length=255)
    reason = models.IntegerField(null=True, blank=True)

    # CRM fields
    transaction = models.OneToOneField('finance.Transaction', CASCADE)

    objects = TransactionPaymeQuerySet.as_manager()

    class Meta:
        db_table = 'finance_transaction_payme'
        verbose_name = 'Транзакция Payme'
        verbose_name_plural = 'Транзакции Payme'
