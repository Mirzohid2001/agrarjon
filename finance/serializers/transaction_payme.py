from datetime import datetime
from rest_framework import serializers

from finance.models import TransactionPayme


class TransactionPaymeSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['wid'] = instance.trans_id
        data['time'] = int(
            datetime.strptime(instance.created_at.strftime("%d.%m.%Y %H:%M:%S,%f"), "%d.%m.%Y %H:%M:%S,%f")
            .strftime('%s')
        ) * 1000
        data['account'] = {'order_id': instance.transaction.order.id}
        data['create_time'] = data['time']
        data['perform_time'] = int(
            datetime.strptime(instance.perform_time.strftime("%d.%m.%Y %H:%M:%S,%f"), "%d.%m.%Y %H:%M:%S,%f")
            .strftime('%s')
        ) * 1000 if instance.perform_time else 0
        data['cancel_time'] = int(
            datetime.strptime(instance.cancel_time.strftime("%d.%m.%Y %H:%M:%S,%f"), "%d.%m.%Y %H:%M:%S,%f")
            .strftime('%s')
        ) * 1000 if instance.cancel_time else 0
        # data['transaction'] = instance.transaction_id

        return data

    class Meta:
        model = TransactionPayme
        fields = (
            'time',
            'amount',
            'perform_time',
            'cancel_time',
            'state',
            'reason',
        )
