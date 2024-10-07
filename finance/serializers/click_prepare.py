from rest_framework import serializers

from finance.models import TransactionsClick


class ClickPrepareSerializers(serializers.ModelSerializer):
    class Meta:
        model = TransactionsClick
        fields = (
            'click_trans_id',
            'merchant_trans_id',
            'merchant_prepare_id',
            'error',
            'error_note',
        )
