from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path('sample', views.index, name='index'),
    path('sample/hello', views.hello, name='hello'),
    path('sample/contact', views.contact, name='contact'),
    path('sample/htmx_contact_form', views.ContactFormHtmxView.as_view(), name='htmx_contact_form'),
]


router = routers.SimpleRouter(trailing_slash=True)
router.register(r'sample/attribute', views.AttributeViewSet, basename='attribute')
router.register(r'sample/operation', views.OperationViewSet, basename='operation')
router.register(r'sample/basic-operation', views.BasicOperationViewSet, basename='basic-operation')
router.register(r'sample/informationpack', views.InformationPackViewSet, basename='informationpack')
urlpatterns += router.urls