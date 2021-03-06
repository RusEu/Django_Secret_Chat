from django.db import models

# Create your models here.
class ChatRoom(models.Model):
	chat_id = models.CharField(max_length = 70)
	chat_name = models.TextField(default = "Error")
	username = models.TextField(blank=True,null=True)
	message = models.TextField(blank=True,null=True)
	time = models.DateTimeField(auto_now=True)
	online_users = models.TextField(blank=True,null=True)
	def usernames(self):
		return self.online_users.split(',')
	def __unicode__(self):
		return  str(self.chat_id) + " / " + str(self.time)