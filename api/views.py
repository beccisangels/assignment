from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .models import Message, User
from .serializers import Message, MessageSerializer, User, UserSerializer

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

    @action(methods=["DELETE"], detail =False, )
    def delete(self, request:Request):
        delete_id =request.data
        delete_messages = self.queryset.filter(id__in=delete_id)
        
        delete_messages.delete()
        return Response( self.serializer_class(delete_messages, many=True).data) 

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

