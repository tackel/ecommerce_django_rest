from django.urls import path

from apps.products.api.viewsets.general_views import MeasureUnitListAPIView,IndicatorListAPIView,CategoryProductListAPIView
from apps.products.api.viewsets.product_views import (
    ProductListCreateAPIView,ProductRetrieveUpdateDestroyAPIView
)
# usando GenericViewSet en la vista de user ya no necesito estas urls sino el ruters
urlpatterns = [
    path('measure_unit/', MeasureUnitListAPIView.as_view(), name = 'measure_unit'),
    path('indicator/', IndicatorListAPIView.as_view(), name = 'indicator'),    
]