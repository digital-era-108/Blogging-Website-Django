from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # Showing Blog
    # path('content/<slug>/', views.post_content, name='content'),
    path('content/<slug:slug>/', views.PostDetailView.as_view(), name='content'),
    
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    # Search Blog
    path('post-search/', views.post_search, name='post_search'),
    # tags & categories
    path('tag/<slug>/', views.tag, name='tag'),
    path('category/<slug>/', views.category, name='category'),
    # Json
    path('posts-json/<int:num_posts>/', views.post_Json.as_view(), name='posts-json'),
    # news-letter
    path('news-letter/', views.news_letter, name='news-letter'),
    # Comment
    path('comment/', views.comment, name='comment'),
    path('reply/', views.reply, name='reply'),
    path('contact-us/', views.contact_us, name='contact'),
    
    # Menu Url
    path('resources/', views.resources, name='resources'),
    path('remove-cache/', views.remove_cache, name='removecache'),

]


# add a flag for
# handling the 404 error
# handler404 = 'webApp.views.error_404_view'