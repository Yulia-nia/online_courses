from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View
from django.urls import reverse
from chat.forms import MessageForm
from chat.models import Chat
from course.models import Course


class DialogsView(View):
    def get(self, request, c_id):
        chats = Chat.objects.filter(members__in=[request.user.id], course_id=c_id)
        course = Course.objects.get(id=c_id)
        return render(request, 'chat/dialogs.html', {'user_profile': request.user, 'chats': chats,
                                                     'course': course})


class MessagesView(View):
    def get(self, request, chat_id, id):
        try:
            course = Course.objects.get(id=id)
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'chat/messages.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'course':course,
                'form': MessageForm()
            }
        )

    def post(self, request, chat_id, id):
        chat = Chat.objects.get(id=chat_id)
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
            form = MessageForm()
        return render(request, "chat/messages.html", {'chat_id': chat_id,
                                                      "form": form,
                                                      'course': Course.objects.get(id=id),
                                                      "chat": chat})


class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id],
                                    type=Chat.DIALOG) # .annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return render(request, "chat/messages.html", {'chat_id': chat.id})
    # redirect(reverse('chat/messages' 'chat/messages.html', kwargs={'chat_id': chat.id}))
