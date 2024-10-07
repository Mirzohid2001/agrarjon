from datetime import datetime
from rest_framework.response import Response
from finance.models import TransactionPayme, Transaction


def cancel_transaction(params):
    transaction = TransactionPayme.objects.select_related('transaction').filter(trans_id=params.get('id')).first()

    if not transaction:
        return Response({
            "error": {
                "code": -31003,
                "message": {
                    "ru": "Несуществующий заказ.",
                    "uz": "Buyurtma topilmadi.",
                    "en": "Defunct order."
                },
                "data": "transaction not found.",
            }
        })

    if int(transaction.state) == -1:
        return Response({
            "result": {
                "transaction": transaction.trans_id,
                "cancel_time": int(transaction.cancel_time.timestamp() * 1000),
                "state": int(transaction.state)
            }
        })

    if int(transaction.state) == 1:
        transaction.state = -1
        transaction.cancel_time = datetime.now()
        transaction.reason = params.get('reason', 0)
        transaction.save()
        transaction.transaction.state = -1
        transaction.transaction.save()
        return Response({
            "result": {
                "transaction": transaction.trans_id,
                "cancel_time": int(transaction.cancel_time.timestamp() * 1000),
                "state": int(transaction.state)
            }
        })

    if int(transaction.state) == 2:
        transaction.state = -2
        transaction.cancel_time = datetime.now()
        transaction.reason = params.get('reason', 0)
        transaction.save()
        transaction.transaction.state = -2
        transaction.transaction.save()
        return Response({
            "result": {
                "transaction": transaction.trans_id,
                "cancel_time": int(transaction.cancel_time.timestamp() * 1000),
                "state": int(transaction.state)
            }
        })

    return Response({
        "result": {
            "transaction": transaction.trans_id,
            "cancel_time": int(transaction.cancel_time.timestamp() * 1000) if transaction.cancel_time else 0,
            "state": int(transaction.state)
        }
    })
