from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Receipt
from .serializers import ReceiptSerializer
from .permissions import IsReceiptOwner


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_summary='Gets receipt list',
        operation_description=(
            'Retrieve an array of receipts owned by the authenticated user.'
        )
    )
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_summary='Gets a receipt',
        operation_description='Retrieve a receipt owned by the authenticated user.'
    )
)
@method_decorator(
    name='update',
    decorator=swagger_auto_schema(
        operation_summary='Updates a receipt',
        operation_description=(
            'Update a receipt owned by the authenticated user. Accepts the ' \
            'following PUT parameters: `buyer`, `seller`, and `items`.'
        )
    )
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        operation_summary='Partially updates a receipt',
        operation_description=(
            'Patch a receipt owned by the authenticated user. Accepts one of ' \
            ' the following PATCH parameters: `buyer`, `seller`, and `items`.'
        )
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_summary='Delete a receipt',
        operation_description='Delete a receipt owned by the authenticated user.'
    )
)
class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated, IsReceiptOwner]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

    @swagger_auto_schema(
        operation_summary='Creates multiple receipts',
        operation_description=(
            'Accept an array of the following POST parameters: ' \
            '`buyer`, `seller`, and `items`.'
        ),
        request_body=ReceiptSerializer(many=True)
    )
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

    @swagger_auto_schema(
        operation_summary='Downloads a PDF receipt',
        operation_description=(
            'Downloads a receipt PDF file owned by the authenticated user. ' \
            'If the PDF is still getting generated, it returns `404 Not Found`.'
        ),
        responses={
            200: 'Receipt.pdf file',
            404: 'Not Found. (PDF generation in progress)'
        }
    )
    @action(detail=True)
    def download(self, request, *args, **kwargs):
        receipt = self.get_object()
        if not receipt.pdf_file:
            return Response({
                'Not Found:': 'Your receipt is being generated. Try again later.'
            }, status=HTTP_404_NOT_FOUND)
        response = HttpResponse(receipt.pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Receipt.pdf"'
        return response
