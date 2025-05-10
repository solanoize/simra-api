
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path("signin/", obtain_auth_token, name='signin')
]
