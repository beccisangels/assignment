from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .models import Message, User
from .serializers import Message, MessageSerializer, User, UserSerializer
from django.views import View
from django.shortcuts import redirect
from rest_framework.views import APIView

from django.shortcuts import render
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import json
from django.http import HttpResponse

class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()
        #.order_by('date_sent').values()
        user = self.request.query_params.get('user')
        if user is not None:
            queryset = queryset.filter(recipient=user)
        return queryset

class MessageView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def delete(self, request):
        ids = request.data.get('ids')
        queryset = self.get_queryset().filter(id__in=ids)
        queryset.destroy()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer



@api_view(['GET', 'DELETE'])
def delete_albums(request):
    """
        GET:    list all messages
        DELETE: delete multiple messages
    """

    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        ids = request.data
        albums = Message.objects.filter(id__in=ids)
        for album in albums:
            album.delete()
        serializer = MessageSerializer(albums, many=True)
        return Response(serializer.data)


class Product_View(View):
    def get(self, request):
        print("HEJHEJ")
        print(self)
        print(request)
        allproduct = Message.objects.all()
        context = {
            'products':allproduct
        }
        
        return render(request, "product/index.html", context)

    #@api_view(('POST',))
    #@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
    def post(self, request, *args, **kwargs):
        print("TESTPRINT")
        if request.method=="POST":
            #product_ids=request.POST.getlist('id[]')
            #product_ids=request.POST.get('id')
            json_ids = json.loads(request.body)

            """
            http://127.0.0.1:8000/delete/
            {
                "id": [1,2,3]
            }
            """
            albums = Message.objects.filter(id__in=json_ids["id"])
            for album in albums:
                album.delete()
            serializer = MessageSerializer(albums, many=True)
            #return Response(serializer.data)
            return HttpResponse()


class DeleteProducts(View):
    def post(self, request, *args, **kwargs):
        products = self.request.POST.getlist('product')
        Message.objects.filter(pk__in=products).delete()
        return redirect('/')

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

class UpdateDeleteMess(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    def get(self, request, pk_ids):
        ids = [int(pk) for pk in pk_ids.split(',')]
        meesageObject = Message.objects.filter(id__in=ids)
        serializeMessageObject = MessageSerializer(meesageObject, many=True)
        return Response(serializeMessageObject.data)

    def delete(self, request, pk_ids):
        ids = [int(pk) for pk in pk_ids.split(',')]
        for i in ids:
            get_object_or_404(Message, pk=i).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

