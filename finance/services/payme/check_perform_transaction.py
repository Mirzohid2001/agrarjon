from rest_framework.response import Response

from finance.models import Transaction


def check_perform_transaction(order, amount: int):
    if not order:
        return Response({
            "error": {
                "code": -31099,
                "message": {
                    "ru": "Несуществующий заказ.",
                    "uz": "Buyurtma topilmadi.",
                    "en": "Defunct order."
                },
                "data": "order"
            },
        })

    return Response({
        "result": {
            "allow": True,
            "additional": {
                "user_id": f"Клиент - {order.user.first_name}",
                "order": f"Заказ - {order.id}",
            },
            "detail": {
                "receipt_type": 0,
                "items": [
                    {
                        "title": "Оплата за заказа",
                        "price": amount,
                        "count": 1,
                        "code": '10801001001000000',
                        "package_code": '1236053',
                        "vat_percent": 0
                    }
                ]
            }
        }
    })
