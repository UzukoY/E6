from rest_framework import viewsets, permissions
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, UserSerializer
from django.contrib.auth.models import User

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chat = serializer.save()
        chat.users.add(self.request.user)

    def get_queryset(self):
        # Показывать только чаты, в которых участвует текущий пользователь
        return Chat.objects.filter(users=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)