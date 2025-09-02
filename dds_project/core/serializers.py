from rest_framework import serializers
from .models import MovementType, Status, Category, Subcategory, Transaction

class MovementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementType
        fields = ['id', 'name', 'slug']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'type']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug', 'category']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'created_at', 'date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment'
        ]
        read_only_fields = ['created_at']

    def validate(self, attrs):
        type_id = attrs.get('type') or getattr(self.instance, 'type', None)
        category = attrs.get('category') or getattr(self.instance, 'category', None)
        subcategory = attrs.get('subcategory') or getattr(self.instance, 'subcategory', None)
        amount = attrs.get('amount') or getattr(self.instance, 'amount', None)

        errors = {}
        if amount is not None and amount <= 0:
            errors['amount'] = 'Сумма должна быть больше нуля.'
        if category and type_id and category.type_id != (type_id.id if hasattr(type_id, 'id') else type_id):
            errors['category'] = 'Категория не относится к выбранному типу.'
        if subcategory and category and subcategory.category_id != category.id:
            errors['subcategory'] = 'Подкатегория не относится к выбранной категории.'
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
