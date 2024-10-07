from datetime import datetime

from rest_framework.response import Response

from finance.models import TransactionPayme, Transaction


def create_transaction(params, order, amount: int):
    trans_id = params.get('id')
    time = params.get('time')
    date = datetime.fromtimestamp(time / 1000)
    transaction_payme = TransactionPayme.objects.filter(trans_id=trans_id).first()
    transaction_crm = Transaction.objects.filter(order_id=order.id).first()
    transaction_id = transaction_crm and TransactionPayme.objects.filter(transaction_id=transaction_crm.id).first()

    if not order:
        return Response({
            "error": {
                "code": -31099,
                "message": {
                    "ru": "Несуществующий заказ.",
                    "uz": "Buyurtma topilmadi.",
                    "en": "Defunct order."
                },
                "data": "user"
            },
        })

    if transaction_crm and trans_id != transaction_id.trans_id:
        return Response({
            "error": {
                "code": -31050,
                "message": {
                    "ru": "существующий заказ.",
                    "uz": "Bunday buyurtma mavjud.",
                    "en": "Defunct order."
                },
                "id": transaction_id.trans_id,
                "data": "transaction"
            },
        })

    if transaction_payme and transaction_payme.trans_id == trans_id:
        return Response({
            "result": {
                "create_time": int(transaction_payme.created_at.timestamp() * 1000),
                "transaction": transaction_payme.trans_id,
                "state": int(transaction_payme.state)
            }
        })

    description = f"Клиент '{order.user.first_name}' оплатил за {order.id} заказа"

    crm_transaction = Transaction.objects.create(
        order_id=order.id,
        type=Transaction.CARD,
        description=description,
        amount=amount / 100,
    )

    transaction, _ = TransactionPayme.objects.update_or_create(
        transaction__order_id=order.id,
        defaults={
            'trans_id': trans_id,
            'amount': amount / 100,
            'time': date,
            'transaction_id': crm_transaction.id
        }
    )

    return Response({
        "result": {
            "create_time": int(transaction.created_at.timestamp() * 1000),
            "transaction": transaction.trans_id,
            "state": int(transaction.state)
        }
    })
