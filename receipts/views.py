from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from .models import Receipt
from .serializers import ReceiptSerializer


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ReceiptSerializer(
            many=True,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        receipt = self.get_object()
        response = HttpResponse(receipt.pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Receipt.pdf"'
        return response
