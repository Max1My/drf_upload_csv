from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from main.views import HospitalViewSet, UploadFileView

router = routers.DefaultRouter()
router.register('hospital', HospitalViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('upload/', UploadFileView.as_view(), name='upload-file')
]
