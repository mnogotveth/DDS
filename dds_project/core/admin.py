from django.contrib import admin
from django import forms
from .models import MovementType, Status, Category, Subcategory, Transaction

@admin.register(MovementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'created_at')
    search_fields = ('name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'created_at')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'created_at')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)

class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

    class Media:
        js = ('core/js/transaction_admin.js',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    list_display = ('date', 'status', 'type', 'category', 'subcategory', 'amount', 'short_comment')
    list_filter = (('date', admin.DateFieldListFilter), 'status', 'type', 'category', 'subcategory')
    search_fields = ('comment',)
    ordering = ('-date', '-id')

    def short_comment(self, obj):
        return (obj.comment[:40] + '…') if obj.comment and len(obj.comment) > 40 else obj.comment
    short_comment.short_description = 'Комментарий'
