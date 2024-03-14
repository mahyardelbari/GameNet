from django.urls import path
from .views import dashboard,  register, verify

urlpatterns = [
	path('', register, name='register'),
	path('verify/', verify, name='verify'),
	path('dashboard/', dashboard, name='dashboard')
]

