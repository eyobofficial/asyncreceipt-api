from rest_framework import serializers

from .models import Receipt, ReceiptItem


class ReceiptItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiptItem
        fields = ['id', 'service', 'unit', 'rate', 'quantity', 'amount']


class ReceiptSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    items = ReceiptItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = ['id', 'seller', 'buyer', 'owner', 'date', 'items', 'total']

    def create(self, validated_data):
        """Creates multiple receipt item instances."""
        items = validated_data.pop('items')
        obj = Receipt.objects.create(**validated_data)
        ReceiptItem.objects.bulk_create(
            [ReceiptItem(receipt=obj, **item) for item in items]
        )
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

        return instance
