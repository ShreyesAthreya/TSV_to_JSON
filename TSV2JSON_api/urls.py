from django.urls import path, include
from rest_framework import routers

from . import views
from .views import OrderViewSet

router = routers.SimpleRouter()
router.register(r'', OrderViewSet, basename='tsv')

urlpatterns = [
    # path('/', views.home),
    path('', include(router.urls)),

    path('get_orders/', OrderViewSet.as_view({'get': 'get_orders'}), name='get_orders'),
    path('get_orders/<int:pk>/', OrderViewSet.as_view({'get': 'get_orders'})),

    path('', OrderViewSet.as_view({'get': 'process_orders'}), name='process_orders'),
    path('process_orders/', OrderViewSet.as_view({'post': 'process_orders'}), name='process_orders'),
]
