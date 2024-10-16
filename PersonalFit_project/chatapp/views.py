from django.shortcuts import render
from .models import ChatRoom, ChatMessage
from users.models import Profile, Client, Trainer
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    profile = Profile.objects.get(user=request.user)

    if profile.is_trainer:
        trainer = Trainer.objects.get(profile=profile)
        clients = Client.objects.filter(trainer=trainer)

        client_chatrooms = []
        for client in clients:
            chatroom = ChatRoom.objects.filter(
                name=client.profile.user.username
            ).first()

            if chatroom:
                unread_count = ChatMessage.objects.filter(
                    room=chatroom, is_read=False
                ).count()
                last_message = (
                    ChatMessage.objects.filter(room=chatroom).order_by("-date").first()
                )
                client_chatrooms.append(
                    {
                        "chatroom": chatroom,
                        "unread_count": unread_count,
                        "last_message": last_message.date if last_message else None,
                    }
                )
        client_chatrooms = sorted(
            client_chatrooms, key=lambda x: x["last_message"] or "", reverse=True
        )
    else:
        clients = None
        client_chatrooms = []

    return render(request, "chatapp/index.html", {"client_chatrooms": client_chatrooms})


def chatroom(request, slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    messages = ChatMessage.objects.filter(room=chatroom)[0:30]

    username = User.objects.get(username=chatroom)
    profile = Profile.objects.get(user=username)
    client = Client.objects.get(profile=profile)
    trainer_name = client.trainer
    is_trainer = profile.is_trainer

    ChatMessage.objects.filter(room=chatroom, is_read=False).update(is_read=True)

    return render(
        request,
        "chatapp/room.html",
        {
            "chatroom": chatroom,
            "messages": messages,
            "trainer_name": trainer_name,
            "is_trainer": is_trainer,
            "client": client,
        },
    )
