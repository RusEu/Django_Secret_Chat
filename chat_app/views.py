from django.shortcuts import render,render_to_response
from django.template import RequestContext
import hashlib
from django.core.cache import cache
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def index(request):
	return render_to_response("index.html",context_instance=RequestContext(request))

def friend_message(request,friend):
	form = IdeaForm()
	username=request.user.id
	friend = str(friend)
	message= Message.objects.all().filter(receiver__user=username)
	i=0
	senders_list = []
	for item in message:
		senders_list.append(item.sender.user.username)
	senders = {}
	for e in senders_list:
		senders[e] = 1
	sender_id = User.objects.get(username = friend).pk
	cofifi_receiver_id = CofifiUser.objects.get(user = username)
	cofifi_sender_id = CofifiUser.objects.get(user = sender_id)
	receiver_id = username
	if request.method == "POST":
		for item in request.POST:
			print item
		text = request.POST.get('text')
		if receiver_id < sender_id:
			last_message_chat = ChatRoom.objects.create(chat_id=str(receiver_id)+"X"+str(sender_id),username=cofifi_receiver_id,message=text)
		else:
			last_message_chat = ChatRoom.objects.create(chat_id=str(sender_id)+"X"+str(receiver_id),username=cofifi_receiver_id,message=text)
	if receiver_id < sender_id:
		messages = ChatRoom.objects.filter(chat_id=str(receiver_id)+"X"+str(sender_id))
	else:
		messages = ChatRoom.objects.filter(chat_id=str(sender_id)+"X"+str(receiver_id))
	context={
	"form":form,
	"messages":messages,
	"online_users":online_users,
	"friend":friend,
	}
	return render_to_response("home.html",context,RequestContext(request))

def add_chat(request):
	if request.method == "POST":
		channel = str(request.POST.get('ChatName'))
		encoded = int(hashlib.sha1(channel).hexdigest(), 16) % (10 ** 8)
		return HttpResponseRedirect("/chat/"+encoded+"/")
	else:
		return HttpResponse("Nothing")

def chat(request,pk):
	print decryption(str(pk))
	context = {
		
	}
	return render_to_response("chat.html",context,context_instance=RequestContext(request))