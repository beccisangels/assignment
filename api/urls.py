from django.urls import path
from .views import MessageList, MessageDetail, UserList, UserDetail, MessageViewSet, MessageView, UpdateDeleteMess, delete

urlpatterns = [
    path('message/', MessageList.as_view()),
    path('message/<int:pk>', MessageDetail.as_view()),
    path('user/', UserList.as_view()),
    path('user/<int:pk>', UserDetail.as_view()),
    path('messages/', MessageViewSet.as_view({'get': 'list'})),
    path('deletemess/', MessageView.as_view()),
    path('mess/', UpdateDeleteMess.as_view({'get': 'list'})),
    path('mess/<str:pk_ids>/', UpdateDeleteMess.as_view({'get': 'list'})),
    path('delete/<str:id>/', delete, name="delete")
]
