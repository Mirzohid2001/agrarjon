from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from finance.services.payme.cancel_transaction import cancel_transaction
from finance.services.payme.check_perform_transaction import check_perform_transaction
from finance.services.payme.check_transaction import check_transaction
from finance.services.payme.create_transaction import create_transaction
from finance.services.payme.get_statement import get_statement
from finance.services.payme.perform_transaction import perform_transaction
from finance.utils.check_basic_auth import check_basic_auth
from blog.models import Order


class TransactionPaymeListView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.headers.get('Authorization')
        hasPermission = check_basic_auth(token)

        if hasPermission:
            return hasPermission

        method = request.data.get('method')
        params = request.data.get('params', {})
        amount = params.get('amount', {})
        account = params.get('account', {})
        order_id = account.get('order_id', None)
        order = Order.objects.filter(id=order_id).first()

        if method == 'CheckPerformTransaction':
            return check_perform_transaction(order, amount)

        if method == 'CreateTransaction':
            return create_transaction(params, order, amount)

        if method == 'PerformTransaction':
            return perform_transaction(request)

        if method == 'CancelTransaction':
            return cancel_transaction(params)

        if method == 'CheckTransaction':
            return check_transaction(params)

        if method == 'GetStatement':
            return get_statement(params)

        return Response()
