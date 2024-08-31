from django.db.models import Count
from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import ListView
from .models import Articles, Pages, Comment
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.db.models import Q
from taggit.models import Tag
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView,HitCountMixin
 

class ArticlesMixinDetailView(object):
    model = Articles
    def get_context_data(self, **kwargs):
        context = super(ArticlesMixinDetailView, self).get_context_data(**kwargs)
        context['post_list'] = Articles.objects.all()[:5]
        context['post_views'] = ["ajax", "detail", "detail-with-count"]
        return context

def articles_list(request, tag_slug=None):
    object_list = Articles.objects.filter(status=1)
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    return render(request,
                 'content_list.html',
                 {'page': page,
                  'articles': articles,
                  'tag': tag})

def articles_comment(request, post_id):
    articles = get_object_or_404(Articles, id=post_id, status=articles.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.articles = articles
        comment.save()
    return render(request, 'comment.html',{'articles': articles,'form': form,'comment': comment})


## detail FBV
def article_detail(request,year,month,day,slug):
    articles = get_object_or_404(Articles,slug=slug,published__year=year,published__month=month,published__day=day)
    comments = articles.comments.filter(active=True)
    new_comment = None
    
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(articles)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
  
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.articles = articles
            new_comment.save()
           
            return redirect(articles.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()
        articles_tags_ids = articles.tags.values_list('id', flat=True)
        similar_articles = Articles.publishedx.filter(tags__in=articles_tags_ids).exclude(id=articles.id)
        similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags','-published')[:4]
        
    return render(request,'article_detail.html',
                  {'articles':articles,
                   'comments':comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                    'similar_articles':similar_articles,
                    })

# handling reply, reply view
def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)
        
        # print(form)

        if form.is_valid():
     
            reply = form.save(commit=False)
           
            post_id = request.POST.get('post_id')  
            parent_id = request.POST.get('parent')   
            post_url = request.POST.get('post_url')   

            print(post_id)
            print(parent_id)
            print(post_url)


            reply = form.save(commit=False)
    
            reply.articles = Articles(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url+'#'+str(reply.id))
            # return render(request,'x.html',{'post_id':post_id,'parent_id':parent_id,'post_url':post_url})
            # return HttpResponse()

    return redirect("/")

### CBV
class ArticleDetail(ArticlesMixinDetailView,HitCountDetailView):
    model =  Articles
    template_name = 'article_detail.html'
    count_hit = True

###

class HomeView(ListView):
    model = Articles
    queryset = Articles.objects.filter(status=1).order_by('-published')       
    context_object_name = 'articles'
    paginate_by = 4    
    template_name = 'home.html'
   
 
class ArticleTags(ListView):
    model = Articles
    template_name = 'search.html'

    def get_queryset(self):  
        query = self.request.GET.get('q')
        object_list = Articles.objects.filter(
            Q(tags__icontains=query) 
        )
        return object_list

class ArticleSearch(ListView):
    model = Articles
    template_name = 'search.html'

    def get_queryset(self):  
        query = self.request.GET.get('q')
        object_list = Articles.objects.filter(
            Q(title__icontains=query) 
        )
        return object_list
    
class MyPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise

class ServicesView(ListView):
    model = Pages
    queryset = Pages.objects.filter(slug='services') 
    context_object_name = 'about'
    template_name = 'pages.html'

class AboutView(ListView):
    model = Pages
    queryset = Pages.objects.filter(slug='about-me') 
    context_object_name = 'about'
    template_name = 'pages.html'

class ContactView(ListView):
    model = Pages
    queryset = Pages.objects.filter(slug='contact-me') 
    context_object_name = 'contact'
    template_name = 'pages.html'

class DisclaimerView(ListView):
    model = Pages
    queryset = Pages.objects.filter(slug='disclaimer') 
    context_object_name = 'disclaimer'
    template_name = 'pages.html'
    
class PrivacyView(ListView):
    model = Pages
    queryset = Pages.objects.filter(slug='privacy-policy') 
    context_object_name = 'privacy'
    template_name = 'pages.html'


