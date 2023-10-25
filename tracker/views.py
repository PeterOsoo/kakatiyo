from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import login as auth_login, logout
from django.shortcuts import render, redirect

from .decorators import redirect_logged_in_user


from .models import Expense
from .forms import ExpenseForm, CustomUserCreationForm


def index(request):
    return render(request, 'home.html', {})


@login_required
def expense_list(request):
    # expenses = Expense.objects.all()
    # expenses = Expense.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    return render(request, 'tracker/expense_list.html', {'expenses': expenses})


def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    return render(request, 'tracker/expense_detail.html', {'expense': expense})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/expense_form.html', {'form': form})


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    # Check if the logged-in user is the owner of the expense
    if expense.user != request.user:
        # Handle unauthorized access, e.g., redirect or display an error message
        # Redirect to the expense list or a suitable page
        return redirect('expense_list')

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/expense_form.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'tracker/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')

    def get(self, request, *args, **kwargs):
        expense = self.get_object()
        if expense.user != self.request.user:
            # Redirect to the expense list for unauthorized users
            return redirect('expense_list')
        return super().get(request, *args, **kwargs)


@redirect_logged_in_user
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('expense_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
