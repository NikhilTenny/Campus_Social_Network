from django.shortcuts import redirect, render
from django.views.generic import ListView
from .models import ChatSpace, Message
from users.models import Profile, CustomeUsers
from django.db.models import Q

# View to list all the personal chats of a user
class PersonalChatsView(ListView):
    model = ChatSpace 
    template_name = 'chat/chatslist.html'

    def get_context_data(self, **kwargs):
        context = {}
        user = self.request.user
        context['chat'] = ChatSpace.objects.get_userchat(user)
        other_user = []
        other_user_profile = []
        for i in context['chat']:
            # Getting the message receiving user and their profile
            if i.users.first() == user:
                other_user.append(i.users.last())
                pro = Profile.objects.get(User = i.users.last())
                other_user_profile.append(pro)
            else:
                other_user.append(i.users.first())
                pro = Profile.objects.get(User = i.users.first())
                other_user_profile.append(pro)  
        context['chat'] = zip(other_user,other_user_profile)
        
        return context

# View in which the logged user can chat with another user        
def ChattingView(request,username): 
    user = request.user
    other_user = CustomeUsers.objects.get(username=username)
    other_user_prof = Profile.objects.get(User=other_user)
    chat_obj = ChatSpace.objects.get_or_create_chat(user, other_user)
    chats = ChatSpace.objects.get_userchat(user)        #List of personal chats of the user
    p_chat = []
    p_chat_profile = []
    for i in chats:
        # Getting the message receiving user and their profile
        if i.users.first() == user:
            p_chat.append(i.users.last())
            pro = Profile.objects.get(User = i.users.last())
            p_chat_profile.append(pro)
        else:
            p_chat.append(i.users.first())
            pro = Profile.objects.get(User=i.users.first())
            p_chat_profile.append(pro)  
    
    chats = zip(p_chat, p_chat_profile)

    
    
    msgs = Message.objects.filter(chat = chat_obj) 
       
    context = {
            'chats':chats,
            'other_user':other_user,
            'other_user_prof':other_user_prof,
            'chatspace':chat_obj, 
            'messages':msgs
    }   
    return render(request,'chat/personalchat.html',context)         

#View to clear the messages in a chat
def ClearChatView(request,username):
    user = request.user
    other_user = CustomeUsers.objects.get(username=username)
    chatobj = ChatSpace.objects.get_or_create_chat(user, other_user)
    Message.objects.filter(chat=chatobj).delete()
    return redirect('chat',username)



