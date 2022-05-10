from django.shortcuts import redirect, render
from django.views.generic import ListView
from .models import ChatSpace, Message
from django.contrib import messages
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

# View to clear the messages in a chat
def ClearChatView(request,username):
    user = request.user
    other_user = CustomeUsers.objects.get(username=username)
    chatobj = ChatSpace.objects.get_or_create_chat(user, other_user)
    Message.objects.filter(chat=chatobj).delete()
    return redirect('chat',username)

# View containing the list of discussion rooms
class Dis_roomsView(ListView):
    template_name = 'chat/dis_rooms.html' 
    model = ChatSpace 

    def get_context_data(self, **kwargs):
        context = {}
        # rooms = ChatSpace.objects.filter(type='chatroom')
        rooms = ChatSpace.objects.users_rooms(self.request.user)
        context['rooms'] = rooms
        return context
# View to create a discussion room
def Dis_roomCreateView(request):
    if request.method == 'POST':
        member_list = request.POST.getlist('members')
        room_name = request.POST.get('room_name')
        print(room_name)
        desc = request.POST.get('description')
        room = ChatSpace.objects.create(
            name=room_name,
            description=desc,
            admin=request.user
        )
        if len(member_list) > 0:
            # Add the selected users to the room
            for member in member_list:
                user = CustomeUsers.objects.get(username=member)
                room.users.add(user)
            room.save()    
        if room:
            messages.success(request,"New Discussion room created")
            return redirect('dis_rooms')    
    users = CustomeUsers.objects.filter(is_teacher=True) | CustomeUsers.objects.filter(is_student=True)
    context = {
        'users' : users
    }
    return render(request, 'chat/createdis_room.html', context)  

# Discussion Room View
def Dis_roomView(request, id, username):
    roomobj = ChatSpace.objects.get(id=id)
    messages = Message.objects.filter(chat=roomobj)
    context = {
        'room': roomobj,
        'messages':messages
    }

    return render(request, 'chat/dis_room.html', context)    

# Discussion Room Details
def Dis_room_detailsView(request, id):    
    roomobj = ChatSpace.objects.get(id=id)
    members = roomobj.users.all()
    isadmin = False                      #Flag to check if user is room admin
    admin = roomobj.admin
    if request.user == admin:
        isadmin = True
    context = {
        'room': roomobj,
        'members': members,
        'isadmin':isadmin
    }
    return render(request, 'chat/dis_room_details.html', context)


# Remove a member from Discussion room
def dis_room_remView(request, id, username):
    roomobj = ChatSpace.objects.get(id=id)
    user = CustomeUsers.objects.get(username=username)
    roomobj.users.remove(user)
    roomobj.save()
    messages.warning(request, "Member Removed")
    return redirect('room_details', id)

# Edit discussion room discription or add members to the room
def dis_room_editView(request, id):
    roomobj = ChatSpace.objects.get(id=id)
    members = ChatSpace.objects.get_members_not_in_room(id)

    context = {
        'room':roomobj,
        'members':members
    }
    if request.method == 'POST':
        #Get the room discription, if no discription entered it returns an empty string
        desc = request.POST.get('room_desc',False)  
        # Save the given description if it is different from old description 
        if roomobj.description == desc:
            return render(request, 'chat/dis_room_edit.html', context)
        else: 
            roomobj.description = desc
            roomobj.save() 
            messages.success(request, 'Description updated')
            return render(request, 'chat/dis_room_edit.html', context)
    print(roomobj.users.all())
    return render(request, 'chat/dis_room_edit.html', context)

# Add a member to the discussion room
def dis_room_addView(request, id, username):
    roomobj = ChatSpace.objects.get(id=id)
    new_member = CustomeUsers.objects.get(username=username) 
    roomobj.users.add(new_member)
    roomobj.save()
    messages.success(request, "New Member Added")
    return redirect('room_edit_dis', id)

