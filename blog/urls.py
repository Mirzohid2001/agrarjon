from django.urls import path
from .views import *
urlpatterns = [
    path('userCount/', UserCountAPIView.as_view(),name='userCount'),
    path('legalDocuments/', LegalDocuments.as_view(),name='legalDocuments'),
    path('news/', NewsList.as_view(),name='news'),
    path('news/<int:pk>/', NewsDetail.as_view(),name='newsDetail'),
    path('banner/', BannerList.as_view(),name='banner'),
    path('seed-cost/', CalculateCostAPIView.as_view(), name='seed-cost'),
    path('mems/', MemsList.as_view(), name='mems'),
    path('mems/<int:pk>/', MemsDetails.as_view(), name='memsDetail'),
    path('download-order/', DownloadOrderAPIView.as_view(), name='download-order'),
    path('all-orders/', AllOrdersAPIView.as_view(), name='all-orders'),
    path('info/', InfoAPIView.as_view(), name='info'),
]
