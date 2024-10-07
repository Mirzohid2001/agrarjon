from rest_framework.response import Response

from finance.models import TransactionPayme


def check_transaction(params):
    transaction = TransactionPayme.objects.filter(trans_id=params.get('id')).first()

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

    return Response({
        "result": {
            "create_time": int(transaction.created_at.timestamp() * 1000),
            "perform_time": int(transaction.perform_time.timestamp() * 1000) if transaction.perform_time else 0,
            "cancel_time": int(transaction.cancel_time.timestamp() * 1000) if transaction.cancel_time else 0,
            "transaction": transaction.trans_id,
            "state": int(transaction.state),
            "reason": transaction.reason
        }
    })
