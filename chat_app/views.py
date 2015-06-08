from django.shortcuts import render,render_to_response
from django.template import RequestContext
import hashlib
import json
from django.core.cache import cache
from django.http import HttpResponse,HttpResponseRedirect
from models import ChatRoom

# Create your views here.
def index(request):
	return render_to_response("index.html",context_instance=RequestContext(request))

def message(request,chatid):
	chat = ChatRoom.objects.all().filter(chat_id=chatid).latest('time')
	chat_name = chat.chat_name
	if request.method == "POST":
		for item in request.POST:
			print item
		text = request.POST.get('text')
		print text
		last_message_chat = ChatRoom.objects.create(chat_id=chatid,chat_name=chat_name,username="tralala",message=text,online_users="gicu,ion,vasile")
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
	chat_room = ChatRoom.objects.all().filter(chat_id = chatid).latest('time')
	messages = ChatRoom.objects.all().filter(chat_id=chatid)
	context = {
		"chat_room":chat_room,
		"messages":messages,
	}
	return render_to_response("chat.html",context,context_instance=RequestContext(request))