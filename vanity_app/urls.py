from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login_page', views.login_page),
    path('login', views.login),
    path('logout', views.logout),
    path('register_page', views.register_page),
    path('register', views.register),
    path('services', views.services),
    path('services/info/<int:service_id>', views.service_info),
    path('services/info/<int:service_id>/book', views.book_service),
    path('classes', views.classes),
    path('account/<int:user_id>', views.user_account),
    path('account/<int:user_id>/cancel/<int:appt_id>', views.cancel_appt),
    path('account/', views.not_logged )
]

