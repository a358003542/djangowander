from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from .serializers import ContactFormSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer


def hello(request):
    return HttpResponse('hello')


def index(request):
    return render(request, 'wander_sample/index.html', {})


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def contact(request):
    form = ContactFormSerializer()
    # full page response
    return Response({'form': form}, template_name='wander_sample/contact.html')


class ContactFormHtmxView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        form = ContactFormSerializer()
        return Response({'form': form}, template_name='wander_sample/htmx/contact_form.html')

    def post(self, request):
        form = ContactFormSerializer(data=request.data)
        if form.is_valid():
            return Response({'form': form}, template_name='wander_sample/htmx/contact_confirm.html')
        else:
            return Response({'form': form}, template_name='wander_sample/htmx/contact_form.html')


from rest_framework import viewsets

from .models import Attribute, Operation, BasicOperation, InformationPack
from .serializers import AttributeSerializer, OperationSerializer, BasicOperationSerializer, InformationPackSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer


class BasicOperationViewSet(viewsets.ModelViewSet):
    queryset = BasicOperation.objects.all()
    serializer_class = BasicOperationSerializer


class InformationPackViewSet(viewsets.ModelViewSet):
    queryset = InformationPack.objects.all()
    serializer_class = InformationPackSerializer
