from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Subscribe, Following, Post, Hashtag, Sentiment, PostTag, AddHashtagForm, PostTagForm, SubscribeForm, FollowingForm, PostForm, MyUserCreationForm


# Anonymous views
#################
def index(request):
  if request.user.is_authenticated():
    return home(request)
  else:
    return anon_home(request)

def anon_home(request):
  return render(request, 'micro/public.html')

def stream(request, user_id):
  # See if to present a 'follow' button
  form = None
  if request.user.is_authenticated() and request.user.id != int(user_id):
    try:
      f = Following.objects.get(follower_id=request.user.id,
                                followee_id=user_id)
    except Following.DoesNotExist:
      form = FollowingForm
  user = User.objects.get(pk=user_id)
  post_list = Post.objects.filter(user_id=user_id).order_by('-pub_date')
  paginator = Paginator(post_list, 10)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    posts = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    posts = paginator.page(paginator.num_pages)
  context = {
    'posts' : posts,
    'stream_user' : user,
    'form' : form,
  }
  return render(request, 'micro/stream.html', context)

def register(request):
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    new_user = form.save(commit=True)
    # Log in that user.
    user = authenticate(username=new_user.username,
                        password=form.clean_password2())
    if user is not None:
      login(request, user)
    else:
      raise Exception
    return home(request)
  else:
    form = MyUserCreationForm
  return render(request, 'micro/register.html', {'form' : form})

# Authenticated views
#####################
@login_required
def home(request):
  '''List of recent posts by people I follow'''
  try:
    my_post = Post.objects.filter(user=request.user).order_by('-pub_date')[0]
  except IndexError:
    my_post = None
  follows = [o.followee_id for o in Following.objects.filter(
    follower_id=request.user.id)]
  post_list = Post.objects.filter(
      user_id__in=follows).order_by('-pub_date')[0:10]
  '''List of recent posts with hashtags I am subscribed to'''
  hashtags = [o.hashtag_id for o in Subscribe.objects.filter(subscriber_id=request.user.id)]
  hposts = [o.post_id for o in PostTag.objects.filter(hashtag_id__in=hashtags)]
  hpost_list = Post.objects.filter(id__in=hposts).order_by('-pub_date')[0:10]

  context = {
    'post_list': post_list,
    'my_post' : my_post,
    'post_form' : PostForm,
    'hpost_list': hpost_list
  }
  return render(request, 'micro/home.html', context)

# Allows to post something and shows my most recent posts.
@login_required
def post(request):
  if request.method == 'POST':
    form = PostForm(request.POST)
    new_post = form.save(commit=False)
    new_post.user = request.user
    new_post.pub_date = timezone.now()
    new_post.save()

    # add new Hashtag and PostTag entries
    post_text = new_post.text;
    hashtags = {tag.strip("#") for tag in post_text.split() if tag.startswith("#")}
    for hashtag in hashtags:
      if not (Hashtag.objects.filter(text=hashtag).exists()):
    	h = Hashtag(text=hashtag)
    	h.save()
      h = Hashtag.objects.filter(text=hashtag)[0]
      pt = PostTag(post=new_post, hashtag=h, posttag_date=timezone.now())
      pt.save()

    return home(request)
  else:
    form = PostForm
  return render(request, 'micro/post.html', {'form' : form})

"""
#Basic RPC Implementation, assumes some variables from the above post
def postTag(self, request, context):
  post = request.new_post
  hashtag = request.h
  posttag_date = request.timezone.now()
  #Change port when ready
  channel = grpc.insecure_channel('[::]:8000')
  stub = views_pb2.PostTagStub(channel)
  #I believe basic RPC setup is done, now need to make it save the search, make sure to build proto file
  #Needs the line 'server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))' in main 
  #attempted to add new hashtag entries but didn't work
  #Same as the code to filter hashtag in post, then return it to rpc. So call rpc for string then return and save

  return views_db2.PostSave(returnedPost=post)
"""

@login_required
def follow(request):
  if request.method == 'POST':
    form = FollowingForm(request.POST)
    new_follow = form.save(commit=False)
    new_follow.follower = request.user
    new_follow.follow_date = timezone.now()
    new_follow.save()
    return home(request)
  else:
    form = FollowingForm
    return render(request, 'micro/follow.html', {'form' : form})


# Scalica Modifications
#######################

# Allow users to subscribe to a hashtag
@login_required
def subscribe(request):
  if request.method == 'POST':
    form = SubscribeForm(request.POST)
    new_subscribe = form.save(commit=False)
    new_subscribe.subscriber = request.user
    new_subscribe.subscribe_date = timezone.now()
    new_subscribe.save()
    return home(request)
  else:
    form = SubscribeForm
  return render(request, 'micro/subscribe.html', {'form' : form})

# Allow users to see a list of posts with a hashtag
@login_required
def hashtag(request, view_tag):
# TODO: Implement selecting a hashtag to view
# TODO: Implement displaying posts with a given tag
  view_hashtag = Hashtag.objects.filter(text=view_tag)[0]
  posts = [o.post_id for o in PostTag.objects.filter(hashtag=view_hashtag)]
  post_list = Post.objects.filter(id__in=posts).order_by('-pub_date')[0:10]
  print (post_list)
  return render(request, 'micro/hashtag.html', {'post_list':post_list})

@login_required
def sentiments(request):
  sentiment_data = Sentiment.objects.all().filter()
  return render(request, 'micro/sentiment.html', {'sentiments':sentiment_data})
	# TODO: implement showing data from the sentiments table
	#       the template can hopefully just call the sentiment to string
	#       for all sentiment entries (should be one for each hashtag)


# External Service APIs
#######################

# Add a Hashtag
def add_hashtag(request):
    if request.method == 'POST':
        form = AddHashtagForm(request.POST)
        new_hashtag = form.save(commit=False)
        if not (Hashtag.objects.filter(text=new_hashtag.text).exists()):
            new_hashtag.save()
        return home(request)
    else:
        form = AddHashtagForm
    return render(request, 'micro/add_hashtag.html', {'form' : form})

# Tag a Post
def tag_post(request):
    if request.method == 'POST':
        form = PostTagForm(request.POST)
        new_postTag = form.save(commit=False)
        #new_postTag.post = #How do I reference the post that needs to be linked here?
        new_postTag.posttag_date = timezone.now()
        new_postTag.save()
        return home(request)
    else:
        return
