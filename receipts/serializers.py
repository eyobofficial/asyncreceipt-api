from rest_framework import serializers

from .models import Receipt, ReceiptItem


class ReceiptItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiptItem
        fields = ('id', 'service', 'unit', 'rate', 'quantity', 'amount')


class ReceiptSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    items = ReceiptItemSerializer(many=True)
    pdf = serializers.HyperlinkedIdentityField(view_name='receipt-download')

    class Meta:
        model = Receipt
        fields = (
            'id', 'url', 'seller', 'buyer',
            'owner', 'date', 'items', 'total', 'pdf'
        )

    def create(self, validated_data):
        """Creates multiple receipt item instances."""
        items = validated_data.pop('items')
        obj = Receipt.objects.create(**validated_data)
        ReceiptItem.objects.bulk_create(
            [ReceiptItem(receipt=obj, **item) for item in items]
        )
        obj.generate_pdf()
        return obj

    def update(self, instance, validated_data):
        """Update a single receipt item instance."""
        items = validated_data.pop('items')
        instance.seller = validated_data.get('seller', instance.seller)
        instance.buyer = validated_data.get('buyer', instance.buyer)
        instance.save()

        # Remove and replace old items
        instance.items.all().delete()
        ReceiptItem.objects.bulk_create(
            [ReceiptItem(receipt=instance, **item) for item in items]
        )

        instance.generate_pdf()
        return instance
