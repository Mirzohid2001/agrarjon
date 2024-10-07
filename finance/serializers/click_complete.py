from rest_framework import serializers

from finance.models import TransactionsClick


class ClickCompleteSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['merchant_confirm_id'] = instance.merchant_prepare_id
        return data

    class Meta:
        model = TransactionsClick
        fields = (
            'click_trans_id',
            'merchant_trans_id',
            'error',
            'error_note',
        )
