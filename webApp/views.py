from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.views import View
from django.views.generic.base import RedirectView
# from django.http import HttpResponseRedirect
from django.contrib import messages
from hitcount.views import HitCountDetailView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from webApp.templatetags import extra
from webSett import settings
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache



def home(request):
    main_post = MainBlog.objects.filter(is_active=True)[0:3]
    context = {'main_post':main_post}
    return render(request, 'index.html', context)


class post_Json(View):
    
    def get(self, *args, **kwargs):
        # print(kwargs)
        upper = kwargs.get('num_posts')
        lower = upper - 3
        posts = list(Blog.objects.values().order_by('-created_at'))[lower:upper]
        posts_size = len(Blog.objects.all())
        max_size = True if upper >= posts_size else False
        return JsonResponse({'data':posts, 'max_size':max_size}, safe=True)




# hit counter
class PostDetailView(HitCountDetailView):
    
    model = Blog
    template_name = 'content_page.html'
    context_object_name = 'post'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        slug = kwargs['object']
        
        content = Blog.objects.get(title=slug)
        comment = Comments.objects.filter(blog=content)
        
        all_reply = {}
        for comm in comment:
            if comm.id not in all_reply.keys():
                all_reply[comm.id] = ReplyComment.objects.filter(parent=comm.id)
            else:
                all_reply[comm.id].append(ReplyComment.objects.filter(parent=comm.id))
                
        # print(all_reply)
        related_posts = Blog.objects.exclude(id=content.id).filter(category=content.category)[0:3]
        
        context = {'post':content, 'related_posts':related_posts, 'comments':comment, 'replies':all_reply}
        print('<-------------------------->', kwargs['object'])
        return context
    
    

# def post_content(request, slug):
    
#     content = Blog.objects.get(slug=slug)
#     comment = Comments.objects.filter(blog=content)
    
#     all_reply = {}
#     for comm in comment:
#         if comm.id not in all_reply.keys():
#             all_reply[comm.id] = ReplyComment.objects.filter(parent=comm.id)
#         else:
#             all_reply[comm.id].append(ReplyComment.objects.filter(parent=comm.id))
            
        
#     # print(all_reply)
#     related_posts = Blog.objects.filter(category=content.category)[0:3]
    
#     context = {'post':content, 'related_posts':related_posts, 'comments':comment, 'replies':all_reply}
#     counter = PostDetailView()
#     print(counter)
#     return render(request, 'content_page.html', context)




def privacy_policy(request):
    return render(request, 'privacy_policy.html')


# Search API
def post_search(request):
    
    blog_title = request.GET['search']
    payload = []
    
    if blog_title != "":
        
        objs = Blog.objects.filter(title__icontains=blog_title)
        
        for obj in objs:
            payload.append({
                'title':obj.title,
                'slug':obj.slug
            })
        
        return JsonResponse({
            'status' : True,
            'payload' : payload,
        })
  

def tag(request, slug):
    tag_slug = Tag.objects.get(is_active=True, slug=slug)
    posts = Blog.objects.filter(tag=tag_slug.id)
    
    context = {'posts':posts, 'query':tag_slug.title}
    return render(request, 'search.html', context)


def category(request, slug):
    category_slug = Categories.objects.get(slug=slug)
    posts = Blog.objects.filter(category=category_slug.id)
    
    context = {'posts':posts, 'query':category_slug.title}
    return render(request, 'search.html', context)


def news_letter(request):
    
    if request.method == "POST":
        try:
            email = request.POST['email']
            
            if email == '':
                messages.warning(request, 'Email Required.')
                return redirect('home')
            
            userEmail, created = NewsLetter.objects.get_or_create(email=email)
            
            if created:
                messages.success(request, 'You have benn Subscribed.')
                return redirect('home')
            
            messages.error(request, 'You Already Subscribed.')
            return redirect('home')
                
        except Exception as e:
            print(e)


@login_required(login_url='signin')
def comment(request):
    
    if request.method == 'POST':
        post_comment = request.POST['comment']
        user = request.user
        post_id = request.POST['post-id']
        blog = Blog.objects.get(id=post_id)
        parent_id = request.POST['parent-id']
        
        print(parent_id)
        
        if post_comment == '':
            messages.warning(request, 'Write the Comment.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
        
        userComment = Comments.objects.create(comment=post_comment, user=user, blog=blog)
        userComment.save()
        messages.success(request, 'Your Comment has been Posted Succesfully.')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    

@login_required(login_url='signin')
def reply(request):
    
    if request.method == 'POST':
        reply_comment = request.POST['reply-comment']
        user = request.user
        comment_id = request.POST['comment-id']
        comments = Comments.objects.get(id=comment_id)
        
        if reply_comment == '':
            messages.warning(request, 'Write the Comment.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
        replyComment = ReplyComment.objects.create(reply=reply_comment, user=user, parent=comments)
        replyComment.save()
        messages.success(request, 'Your Reply has been Posted Succesfully.')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def contact_us(request):
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        message = request.POST['message']
        
        owner_name = 'Radhey'
        owner_email = 'radheyrathore555@gmail.com'
        
        subject = f'Receive the email from Info-DigitalEra Contact By {first_name} " " {last_name}'
        message = f'''Hi {owner_name} \n
        {first_name} is Contact You. Contact Email - {email}
        \n
        {message}
        '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [owner_email, ]
        send_mail( subject, message, email_from, recipient_list )
        
        messages.success(request, 'Your Message has been Send.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    return render(request, 'contact.html')

 
 
# def error_404_view(request, exception):
#     return render(request, '404.html')


def resources(request):
    return render(request, 'resources.html')

def remove_cache(request):
    cache.clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))