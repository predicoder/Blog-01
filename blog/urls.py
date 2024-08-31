from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('tag/<slug:tag_slug>/', views.articles_list, name='tag_search'),
    path('about/',ServicesView.as_view(),name='services'),
    path('about/',AboutView.as_view(),name='about'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('disclaimer/',DisclaimerView.as_view(),name='disclaimer'),
    path('privacy/',PrivacyView.as_view(),name='privacy'),
    path('comment/reply/', views.reply_page, name="reply"),
    path('search.html/',ArticleSearch.as_view(),name='search_results'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',views.article_detail,name='article_detail'),
    path('<int:articles_id>/comment/',views.articles_comment, name='articles_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
