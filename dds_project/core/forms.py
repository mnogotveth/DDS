from django import forms
from .models import Transaction, Category, Subcategory

class DateInput(forms.DateInput):
    input_type = 'text'
    attrs = {'placeholder': 'дд.мм.гггг'}

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select', 'id': 'id_type'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-select', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        t = (self.data.get('type') or (self.instance.type_id if self.instance and self.instance.pk else None))
        if t:
            self.fields['category'].queryset = Category.objects.filter(type_id=t).order_by('name')
        else:
            self.fields['category'].queryset = Category.objects.none()

        c = (self.data.get('category') or (self.instance.category_id if self.instance and self.instance.pk else None))
        if c:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=c).order_by('name')
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()
