from django.test import TestCase

from .factories import ReceiptItemFactory, ReceiptFactory


class ReceiptItemTests(TestCase):
    """Unit tests for `ReceiptItem` model objects."""

    def setUp(self):
        self.item = ReceiptItemFactory(rate=2, quantity=10)

    def test_receipt_item_amount(self):
        """
        Ensure `amount` property returns the multiple of
        `rate` & `quantity`.
        """
        expected_result = 20
        self.assertEqual(self.item.amount, expected_result)


class ReceiptTests(TestCase):
    """Unit tests for `Receipt` model objects."""

    def setUp(self):
        self.receipt = ReceiptFactory()
        self.item1 = ReceiptItemFactory(
            receipt=self.receipt,
            rate=2, quantity=10
        )
        self.item2 = ReceiptItemFactory(
            receipt=self.receipt,
            rate=3, quantity=20
        )

    def test_receipt_total(self):
        """
        Ensure `total` property returns the sum of items amount.
        """
        expected_result = 80
        self.assertEqual(self.receipt.total, expected_result)
