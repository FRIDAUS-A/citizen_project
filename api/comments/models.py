from django.db import models
from posts.models import Post
from citizen.models import Citizen

# Create your models here.
class Comment(models.Model):
	comment_id = models.CharField(max_length=255, primary_key=True)
	comment = models.TextField()
	citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		"""
		string representation of the model Post
		"""
		return self.comment