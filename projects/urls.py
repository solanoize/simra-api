
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('catalogs/', include('catalogs.urls', namespace='catalogs')),
    path('budgets/', include('budgets.urls', namespace='budgets')),
]
