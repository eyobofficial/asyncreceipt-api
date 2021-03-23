from unittest import mock

from django.core.files.base import ContentFile
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIRequestFactory

from receipts.models import Receipt, ReceiptItem
from receipts.serializers import ReceiptSerializer
from .factories import UserFactory, ReceiptFactory, ReceiptItemFactory


class ReceiptViewSetTests(APITestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_receipt_create_as_anonymous_user(self):
        """
        Ensure unauthenticated users cannot create receipts.
        """
        url = reverse('receipt-list')
        payload = [
            {
                'seller': 'Test seller',
                'buyer': 'Test buyer',
                'items': [
                    {
                        'service': 'Test service 1',
                        'unit': 'unit',
                        'rate': 2,
                        'quantity': 10
                    },
                    {
                        'service': 'Test service 2',
                        'unit': 'unit',
                        'rate': 3,
                        'quantity': 20
                    }
                ]
            }
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(ReceiptItem.objects.count(), 0)

    @mock.patch(
        'receipts.serializers.generate_receipt_pdf',
        return_value=ContentFile('')
    )
    def test_receipt_create_as_authenticated_user(self, mock_object):
        """
        Ensure authenticated users can create multiple receipts.
        """
        self.client.force_authenticate(self.user1)
        url = reverse('receipt-list')
        payload = [
            {
                'seller': 'Test seller',
                'buyer': 'Test buyer',
                'items': [
                    {
                        'service': 'Test service 1',
                        'unit': 'unit',
                        'rate': 2,
                        'quantity': 10
                    },
                    {
                        'service': 'Test service 2',
                        'unit': 'unit',
                        'rate': 3,
                        'quantity': 20
                    }
                ]
            }
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Receipt.objects.count(), 1)
        self.assertEqual(ReceiptItem.objects.count(), 2)
        self.assertEqual(Receipt.objects.first().owner, self.user1)

    def test_receipt_list_as_anonymous_user(self):
        """
        Ensure unauthenticated users can't access receipt list.
        """
        url = reverse('receipt-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_receipt_list_as_authenticated_user(self):
        """
        Ensure authenticated users can access receipt list owned by them.
        """
        url = reverse('receipt-list')
        self.client.force_authenticate(self.user1)

        # User 1 receipts
        receipt1 = ReceiptFactory(owner=self.user1)
        receipt2 = ReceiptFactory(owner=self.user1)

        qs = Receipt.objects.all()
        request = APIRequestFactory().get(url)
        serializer = ReceiptSerializer(
            qs, many=True,
            context={'request': request}
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_non_own_receipt_list_as_authenticated_user(self):
        """
        Ensure authenticated users cannot access receipt list owned by others.
        """
        url = reverse('receipt-list')
        self.client.force_authenticate(self.user1)

        # User 1 receipts
        receipt1 = ReceiptFactory(owner=self.user2)
        receipt2 = ReceiptFactory(owner=self.user2)

        response = self.client.get(url)
        self.assertEqual(response.data, [])

    def test_receipt_detail_as_anonymous_user(self):
        """
        Ensure unauthenticated users can't access receipt detail.
        """
        receipt = ReceiptFactory()
        url = reverse('receipt-detail', args=[receipt.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_own_receipt_detail_as_authenticated_user(self):
        """
        Ensure authenticated users can access receipt detail owned by them.
        """
        receipt = ReceiptFactory(owner=self.user1)
        url = reverse('receipt-detail', args=[receipt.pk])
        self.client.force_authenticate(self.user1)

        request = APIRequestFactory().get(url)
        serializer = ReceiptSerializer(receipt, context={'request': request})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_non_own_receipt_detail_as_authenticated_user(self):
        """
        Ensure authenticated users can't access receipt detail owned by others.
        """
        receipt = ReceiptFactory(owner=self.user1)
        url = reverse('receipt-detail', args=[receipt.pk])
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
