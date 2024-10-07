from datetime import datetime

from rest_framework.response import Response

from finance.models import TransactionPayme
from finance.serializers.transaction_payme import TransactionPaymeSerializers


def get_statement(params):
    fr = params.get('from')
    to = params.get('to')
    fr_datetime = datetime.fromtimestamp(fr / 1000)
    to_datetime = datetime.fromtimestamp(to / 1000)
    print(fr_datetime, to_datetime)
    transactions = TransactionPayme.objects.filter(time__gte=fr_datetime, time__lte=to_datetime)
    serializer = TransactionPaymeSerializers(instance=transactions, many=True).data

    return Response({
        "result": {
            "transactions": serializer
        }
    })
