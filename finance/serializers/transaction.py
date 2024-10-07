from rest_framework import serializers

from finance.models import Transaction


class SimpleTransactionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user

        if not user:
            raise serializers.ValidationError('User not found.')

        validated_data['type_id'] = 1
        validated_data['student'] = user

        instance = super().create(validated_data)

        return instance

    class Meta:
        model = Transaction
        fields = ('id', 'order')
