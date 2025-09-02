from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MovementType(TimestampedModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Status(TimestampedModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(TimestampedModel):
    type = models.ForeignKey(MovementType, on_delete=models.PROTECT, related_name='categories')
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['type', 'name'], name='uniq_category_per_type')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.type.name})"

class Subcategory(TimestampedModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='subcategories')
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'name'], name='uniq_subcategory_per_category')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Transaction(TimestampedModel):
    date = models.DateField(default=timezone.now)  # можно менять вручную
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='transactions')
    type = models.ForeignKey(MovementType, on_delete=models.PROTECT, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ['-date', '-id']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['status', 'type', 'category', 'subcategory']),
        ]

    def clean(self):
        errors = {}
        if self.amount is not None and self.amount <= 0:
            errors['amount'] = 'Сумма должна быть больше нуля.'
        if self.category_id and self.type_id and self.category.type_id != self.type_id:
            errors['category'] = 'Категория не относится к выбранному типу.'
        if self.subcategory_id and self.category_id and self.subcategory.category_id != self.category_id:
            errors['subcategory'] = 'Подкатегория не относится к выбранной категории.'
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.date} • {self.type} • {self.category}/{self.subcategory} • {self.amount}"
