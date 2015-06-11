from django.shortcuts import render,render_to_response
from django.template import RequestContext
import hashlib
import json
import random
from django.core.cache import cache
from django.http import HttpResponse,HttpResponseRedirect
from models import ChatRoom
from django.contrib.sessions.backends.db import SessionStore

# Create your views here.
def index(request):
	return render_to_response("index.html",context_instance=RequestContext(request))

def chat(request,chatid):
	if 'username' not in request.session:
		request.session['username'] = "user" + str( random.randint(1,9999) )
	else:
		chat_user = request.session['username']
	chat_user = request.session['username']
	chat_room = ChatRoom.objects.all().filter(chat_id = chatid).latest('time')
	if chat_user not in chat_room.online_users :
		users_online = str(chat_room.online_users)+","+str(chat_user)
		welcome = ChatRoom.objects.create(chat_id=chatid,chat_name=chat_room.chat_name,username=request.session['username'],message="I've just entered the chat room",online_users=users_online)
	context = {
		"chat_room":chat_room,
	}
	return render_to_response("chat.html",context,context_instance=RequestContext(request))


def message(request,chatid):
	chat = ChatRoom.objects.all().filter(chat_id=chatid).latest('time')
	chat_name = chat.chat_name
	chat_user = request.session['username']
	if request.method == "POST":
		users_online = chat.online_users
		if chat_user not in chat.online_users:
			users_online = str(chat.online_users)+","+str(chat_user)
		text = request.POST.get('text')
		last_message_chat = ChatRoom.objects.create(chat_id=chatid,chat_name=chat_name,username=chat_user,message=text,online_users=users_online)
	messages= ChatRoom.objects.all().filter(chat_id=chatid).order_by('-time')
	r = messages
	res = []
	for msgs in reversed(r) :
		res.append({'id':msgs.chat_id,'user':str(msgs.username),'msg':msgs.message,'time':msgs.time.strftime('%I:%M:%S %p').lstrip('0')})
	data = json.dumps(res)
	context={
	"messages":messages,
	}
	return HttpResponse(data,content_type="application/json")

def user_list(request,chatid):
	chat = ChatRoom.objects.all().filter(chat_id=chatid).latest('time')
	chat_name = chat.chat_name
	chat_user = request.session['username']
	res = []
	for word in chat.online_users.split(','):
		res.append({'online_users':word})
	data = json.dumps(res)	
	if request.method == "POST":
		user_left_chat = request.POST.get('leftchat')
		if user_left_chat:
			users_online = chat.online_users.replace(","+chat_user, "")
			chat.online_users = chat.online_users.replace(","+chat_user, "");
			chat.save()
			print users_online
			last_message_chat = ChatRoom.objects.create(chat_id=chatid,chat_name=chat_name,username="Administrator",message="User <strong id='leftchat'>"+user_left_chat+"</strong> has left chat",online_users=users_online)
			print last_message_chat.online_users
	context={
		"chat":chat,
	}
	return HttpResponse(data,content_type="application/json")

def add_chat(request):
	if request.method == "POST":
		channel = str(request.POST.get('ChatName'))
		encoded = int(hashlib.sha1(channel).hexdigest(), 16) % (10 ** 14)
		encoded = str(encoded)
		ChatRoom.objects.create(chat_id=encoded,chat_name=channel,username="Administrator",message="Welcome to "+channel,online_users="Administrator")
		ChatRoom.objects.create(chat_id=encoded,chat_name=channel,username="Administrator",message="Share this link with your friends: <br><a>http://127.0.0.1:8000/chat/"+encoded+"/</a>",online_users="Administrator")
		return HttpResponseRedirect("/chat/"+encoded+"/")
	else:
		return HttpResponse("Nothing")

def changeuser(request,chatid):
	chat_user = request.session['username']
	if request.GET:
		chat_room = ChatRoom.objects.all().filter(chat_id = chatid).latest('time')
		if request.GET.get('user') not in chat_room.online_users :
			if chat_room.online_users.find(","+chat_user):
				chat_room.online_users = chat_room.online_users.replace(","+chat_user, "");
			else :
				chat_room.online_users = chat_room.online_users.replace(chat_user, "");
			name = request.GET.get('user')
			request.session['username'] = str(name)
			chat_room.save()
			chat_name = chat_room.chat_name
			notification = "Username "+ str(chat_user) + " has changed name to " + str(name)
			ChatRoom.objects.create(chat_id=chatid,chat_name=chat_name,username="Administrator",message=notification,online_users=chat_room.online_users)
			chat_user = str(name)
			return HttpResponseRedirect('/chat/'+chatid)
		else:
			return HttpResponse("User allready in use")
	else:
		return HttpResponse("Nothing To Change")
def delete_chat(request,chatid):
	ChatRoom.objects.filter(chat_id=chatid).delete()
	return HttpResponseRedirect("/")