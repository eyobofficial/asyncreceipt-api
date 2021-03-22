from django.http import HttpResponse

from celery import shared_task

from .models import Receipt


@shared_task(name='generate_receipt_pdf')
def generate_receipt_pdf(receipt_id):
    """Generate PDF for receipt instance."""
    try:
        receipt = Receipt.objects.get(pk=receipt_id)
        receipt.generate_pdf()
    except Receipt.DoesNotExist:
        pass
