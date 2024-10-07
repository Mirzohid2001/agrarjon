from datetime import datetime

from rest_framework.response import Response

from finance.models import TransactionPayme, Transaction


def perform_transaction(request):
    params = request.data.get('params', {})
    transaction = (TransactionPayme.objects.filter(trans_id=params.get('id')).first())

    if not transaction:
        return Response({
            "error": {
                "code": -31003,
                "message": {
                    "ru": "Несуществующая транзакция.",
                    "uz": "Tranzaksiya topilmadi.",
                    "en": "Transaction not found."
                },
                "data": "transaction not found.",
            }
        })

    state = int(transaction.state)

    if state == -1 or state == -2:
        return Response({
            "error": {
                "code": -31008,
                "message": {
                    "ru": "Ошибка в транзакции.",
                    "uz": "Tranzaksiyada xatolik.",
                    "en": "Problem in transaction."
                },
                "data": "transaction not found.",
            }
        })

    if state == 2:
        return Response({
            "result": {
                "perform_time": int(transaction.perform_time.timestamp() * 1000),
                "transaction": transaction.trans_id,
                "state": 2,
            }
        })

    if state == 1:
        crm_transaction = Transaction.objects.filter(order=transaction.transaction.order).first()

        crm_transaction.state = 2
        crm_transaction.save()

        transaction.state = 2
        transaction.perform_time = datetime.now()
        transaction.transaction_id = crm_transaction.id
        transaction.save()

        return Response({
            "result": {
                "perform_time": int(transaction.perform_time.timestamp() * 1000),
                "transaction": transaction.trans_id,
                "state": 2,
            }
        })

    return Response({
        "error": {
            "code": -31008,
            "message": {
                "ru": "Ошибка в транзакции.",
                "uz": "Tranzaksiyada xatolik.",
                "en": "Problem in transaction."
            },
            "data": "transaction",
        }
    })
