from rest_framework.response import Response
from rest_framework.views import APIView

from finance.serializers.transaction import SimpleTransactionSerializer


class TransactionForClickListView(APIView):
    def post(self, request):
        serializer = SimpleTransactionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data)
