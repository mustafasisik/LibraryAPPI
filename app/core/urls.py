from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.home, name="home"),
    # api endpoints
    path('api/test', views.TestAPI.as_view(), name='test_api'),
    path('api/login', obtain_auth_token, name='login_api'),
    path('api/register_user', views.RegisterUserAPI.as_view(), name='register_user_api'), #ok
    path('api/forget_password', views.ForgetPasswordAPI.as_view(), name='forget_password_api'), #ok
    path('api/reset_password', views.ResetPasswordAPI.as_view(), name='reset_password_api'), # ok
    path('api/create_book', views.CreateBookAPI.as_view(), name='create_book_api'), # ok
    path('api/reserve_book', views.ReserveBookAPI.as_view(), name='reserve_book_api'), # ok
    path('api/return_book', views.ReturnBookAPI.as_view(), name='return_book_api'), # ok
    path('api/delete_book', views.DeleteBookAPI.as_view(), name='delete_book_api'), # ok
    path('api/create_more_book', views.CreateMoreBooksAPI.as_view(), name='create_more_book_api'), # ok
    path('api/remove_all_books', views.RemoveAllBooksAPI.as_view(), name='remove_all_books_api'), # ok
    path('api/reserve_all_books', views.ReserveAllBooksAPI.as_view(), name='reserve_all_books_api'), # ok
    path('api/return_all_books', views.ReturnAllBooksAPI.as_view(), name='return_all_books_api'), # ok
]
