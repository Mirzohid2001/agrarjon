# from rest_framework import serializers
# from finance.models import TransactionCategory
# from core.utils.serializers import ValidatorSerializer
#
#
# class TransactionCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TransactionCategory
#         fields = ('id', 'name', 'default_amount', 'description_template', 'type', 'system_name', 'is_main')
#         extra_kwargs = {'system_name': {'read_only': True}}
#
#
# class TransactionCategoryFilterSerializer(ValidatorSerializer):
#     page = serializers.IntegerField(default=1)
#     size = serializers.IntegerField(default=15)
#     type = serializers.CharField(required=False)
