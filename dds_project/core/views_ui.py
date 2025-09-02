from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.contrib import messages

from .models import Transaction, MovementType, Status, Category, Subcategory
from .forms import TransactionForm

def _parse_date(s: str):
    if not s:
        return None
    for fmt in ('%d.%m.%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None

class TransactionListView(ListView):
    template_name = 'transactions/list.html'
    model = Transaction
    paginate_by = 20

    def get_queryset(self):
        qs = (Transaction.objects
              .select_related('status', 'type', 'category', 'subcategory')
              .all())

        date_from = _parse_date(self.request.GET.get('date_from'))
        date_to   = _parse_date(self.request.GET.get('date_to'))
        status_id = self.request.GET.get('status') or None
        type_id   = self.request.GET.get('type') or None
        cat_id    = self.request.GET.get('category') or None
        sub_id    = self.request.GET.get('subcategory') or None
        search    = self.request.GET.get('search') or None

        if date_from: qs = qs.filter(date__gte=date_from)
        if date_to:   qs = qs.filter(date__lte=date_to)
        if status_id: qs = qs.filter(status_id=status_id)
        if type_id:   qs = qs.filter(type_id=type_id)
        if cat_id:    qs = qs.filter(category_id=cat_id)
        if sub_id:    qs = qs.filter(subcategory_id=sub_id)
        if search:    qs = qs.filter(comment__icontains=search)

        return qs.order_by('-date', '-id')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['statuses'] = Status.objects.order_by('name')
        ctx['types'] = MovementType.objects.order_by('name')
        # категории/подкатегории подгрузим динамически на форме через JS + API
        ctx['params'] = {
            k: self.request.GET.get(k, '')
            for k in ('date_from', 'date_to', 'status', 'type', 'category', 'subcategory', 'search')
        }
        return ctx

class TransactionCreateView(CreateView):
    template_name = 'transactions/form.html'
    form_class = TransactionForm
    success_url = reverse_lazy('ui:transaction_list')

    def form_valid(self, form):
        messages.success(self.request, 'Транзакция создана.')
        return super().form_valid(form)

class TransactionUpdateView(UpdateView):
    template_name = 'transactions/form.html'
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('ui:transaction_list')

    def form_valid(self, form):
        messages.success(self.request, 'Транзакция обновлена.')
        return super().form_valid(form)

class TransactionDeleteView(DeleteView):
    template_name = 'transactions/confirm_delete.html'
    model = Transaction
    success_url = reverse_lazy('ui:transaction_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Транзакция удалена.')
        return super().delete(request, *args, **kwargs)
