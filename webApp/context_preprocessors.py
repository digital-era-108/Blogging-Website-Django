from .models import Tag, Categories, Blog
from hitcount.views import HitCountDetailView


def get_tags(request):
    tags = Tag.objects.filter(is_active=True)[0:8]
    context = {'tags':tags}
    return context    


def get_Categories(request):
    categories = Categories.objects.filter(is_active=True)[0:8]
    trending_categories = Categories.objects.filter(is_active=True, is_trending=True)[0:8]
    context = {'all_categories':categories, 'trend_categories':trending_categories}
    return context    



def popular_Blog(request):
    # Popular Blogs
    blog = Blog.objects.order_by('-hit_count_generic__hits')[0:4]
    # Latest Blogs
    blogs = Blog.objects.all().order_by('-created_at')[0:3]
    context = {'popular_blog':blog, 'blogs':blogs}
    return context


