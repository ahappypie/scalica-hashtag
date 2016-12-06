from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.forms import ModelForm, TextInput

class Post(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  text = models.CharField(max_length=256, default="")
  pub_date = models.DateTimeField('date_posted')
  def __str__(self):
    if len(self.text) < 16:
      desc = self.text
    else:
      desc = self.text[0:16]
    return self.user.username + ':' + desc

class Following(models.Model):
  follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_follows")
  followee = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_followed")
  follow_date = models.DateTimeField('follow data')
  def __str__(self):
    return self.follower.username + "->" + self.followee.username

class Hashtag(models.Model):
  text = models.CharField(max_length=256, default="")
  def __str__(self):
    return "#" + self.text

class PostTag(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
  posttag_date = models.DateTimeField('date')
  def __str__(self):
    return post.__str__() + ':' + hashtag.__str__()

class Sentiment(models.Model):
  hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
  sentiment_analysis = models.CharField(max_length=256, default="")
  sentiment_date = models.DateTimeField('sentiment date')
  def __str__(self):
    return hashtag.__str__() + ":" + sentiment_analysis

class Subscribe(models.Model):
  subscriber = models.ForeignKey(settings.AUTH_USER_MODEL)
  hashtag = models.ForeignKey(Hashtag)
  subscribe_date = models.DateTimeField()
  def __str__(self):
    return self.subscriber.username + "->#" + self.hashtag.text

# Model Forms
class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ('text',)
    widgets = {
      'text': TextInput(attrs={'id' : 'input_post'}),
    }

class AddHashtagForm(ModelForm):
    class Meta:
        model = Hashtag
        fields = ('text',)

class PostTagForm(ModelForm):
    class Meta:
        model = PostTag
        fields = ('hashtag',)

class FollowingForm(ModelForm):
  class Meta:
    model = Following
    fields = ('followee',)

class SubscribeForm(ModelForm):
  class Meta:
    model = Subscribe
    fields = ('hashtag',)

class MyUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    help_texts = {
      'username' : '',
    }
