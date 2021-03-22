from io import BytesIO
from uuid import uuid4

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.functional import cached_property

from weasyprint import HTML


class Receipt(models.Model):
    """Payment receipt"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    seller = models.CharField('seller name', max_length=120)
    buyer = models.CharField('buyer name', max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='receipts'
    )
    pdf_file = models.FileField(
        upload_to='receipts/',
        null=True, blank=True
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-date', )

    def __str__(self):
        return self.buyer

    @cached_property
    def total(self):
        """Returns the total monetary amount of all related items."""
        result = sum(item.amount for item in self.items.all())
        return round(result, 2)

    def generate_pdf(self):
        """Generate a PDF file of the receipt."""
        template = get_template('receipts/placeholder.html')
        context = {'receipt': self}
        html = template.render(context)
        pdf_file = HTML(string=html).write_pdf()
        self.pdf_file.save('receipt.pdf', ContentFile(pdf_file), save=True)


class ReceiptItem(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='items'
    )
    service = models.CharField(max_length=255)
    unit = models.CharField(max_length=100, help_text='Unit of measurement.')
    rate = models.DecimalField('unit rate', max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name ='Receipt Item'
        verbose_name_plural = 'Receipt Items'

    def __str__(self):
        return self.service

    @cached_property
    def amount(self):
        """Returns the monentary amount of the item."""
        return round(self.rate * self.quantity, 2)
