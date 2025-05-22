from django.urls import path
from .views import UserRegistrationView , UserLoginView , CategoryView  , ExpenseView , SingleExpenseView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='register'),
    path('users/login/', UserLoginView.as_view(), name='login'),
    path('users/category/' , CategoryView.as_view() , name='category'),
    path('users/<int:category_id>/category/' , CategoryView.as_view() , name='Update-Delete-Category'),
    path('users/expense/' , ExpenseView.as_view() , name='expense'),
    path('users/<int:expense_id>/expense' , ExpenseView.as_view() , name='Update-Delete-Expnese'),
    path('users/<int:expense_id>/expense' , SingleExpenseView.as_view() , name='singleexpense')
]