from django.shortcuts import render,render_to_response
from django.template import RequestContext
import hashlib
import json
import random
from django.core.cache import cache
from django.http import HttpResponse,HttpResponseRedirect
from models import ChatRoom
from django.contrib.sessions.backends.db import SessionStore


s = SessionStore()
chat_user = s['username'] = "user" + str( random.randint(1,9999) )
s.save()

# Create your views here.
def index(request):
	return render_to_response("index.html",context_instance=RequestContext(request))

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

def add_chat(request):
	if request.method == "POST":
		channel = str(request.POST.get('ChatName'))
		encoded = int(hashlib.sha1(channel).hexdigest(), 16) % (10 ** 8)
		encoded = str(encoded)
		ChatRoom.objects.create(chat_id=encoded,chat_name=channel,username="Administrator",message="Welcome to "+channel,online_users="Administrator")
		return HttpResponseRedirect("/chat/"+encoded+"/")
	else:
		return HttpResponse("Nothing")

def chat(request,chatid):
	s = SessionStore()
	# stored as seconds since epoch since datetimes are not serializable in JSON.
	s['username'] = "user" + str( random.randint(1,9999) )
	s.save()
	chat_user = s['username']
	chat_room = ChatRoom.objects.all().filter(chat_id = chatid).latest('time')
	messages = ChatRoom.objects.all().filter(chat_id=chatid)
	context = {
		"chat_user": chat_user,
		"chat_room":chat_room,
		"messages":messages,
	}
	return render_to_response("chat.html",context,context_instance=RequestContext(request))

def changeuser(request,chatid):
	chat_user = request.session['username']
	if request.GET:
		name = request.GET.get('user')
		s = SessionStore(session_key=request.session.session_key)
		print s.session_key
		s['username'] = str(name)
		s.save()
		chat_room = ChatRoom.objects.all().filter(chat_id = chatid).latest('time')
		chat_name = chat_room.chat_name
		notification = "Username "+ str(chat_user) + " has changed name to " + str(name)
		ChatRoom.objects.create(chat_id=chatid,chat_name=chat_name,username="Administrator",message=notification,online_users=chat_room.online_users)
		chat_user = str(name)
		return HttpResponseRedirect('/chat/'+chatid)
	else:
		return HttpResponse("Nothing To Change")
def delete_chat(request,chatid):
	ChatRoom.objects.filter(chat_id=chatid).delete()
	return HttpResponseRedirect("/")