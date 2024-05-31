from django.urls import path
from .views import *
urlpatterns = [
    path('userCount/', UserCountAPIView.as_view(),name='userCount'),
    path('legalDocuments/', LegalDocuments.as_view(),name='legalDocuments'),
    path('news/', NewsList.as_view(),name='news'),
    path('news/<int:pk>/', NewsDetail.as_view(),name='newsDetail'),
    path('banner/', BannerList.as_view(),name='banner'),
    path('seed-cost/', CalculateCostAPIView.as_view(), name='seed-cost'),

]