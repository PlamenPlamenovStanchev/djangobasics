from datetime import datetime
from idlelib.debugobj import dispatch

from django.db.models import Q
from django.forms import modelform_factory
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView, CreateView, UpdateView, DeleteView, FormView, DetailView, \
    ListView
from django.views.generic.edit import FormMixin

from posts.decorators import measure_execution_time
from posts.forms import SearchForm, PostCreateForm, PostDeleteForm, CommentFormSet
from posts.mixins import TimeRestrictedMixin
from posts.models import Post


def index(request):
    return render(request, 'index.html')


# Simple example of Django under the hood
# class MyView:
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.method == "GET":
#             return self.get(request, *args, **kwargs)
#         ...
#
#     @classonlymethod
#     def as_view(cls):
#
#         def view(request, *args, **kwargs):
#             self = cls()
#             return self.dispatch(request, args, kwargs)
#
#         return view


class IndexView(TemplateView):
#    def dispatch(self, request, *args, **kwargs): overriding the dispatch method with custom logic
#        if request.user.is_authenticated:
#            return super().dispatch(request, *args, **kwargs)
#       return HTTPResponse('403 Forbidden')

#    template_name = 'index.html'  the static way
#    extra_context = {
#        "current_time": datetime.now(),
#    }

    def get_context_data(self, **kwargs): # the dynamic way
        super().get_context_data(**kwargs)
        kwargs.update({
            "current_time": datetime.now()
        })
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


    def get_template_names(self):
        if self.request.user.is_superuser:
            return ['index_for_admin.html']

        return ['index.html']



#    if request.method == 'GET':
#       form = MyForm()
#   else:
#       form = MyForm(request.POST)
#
#   form = MyForm(request.POST or None)

#   if request.method == 'POST' and form.is_valid():
#        print('The data is', request.POST.get('my_text'))
#        print('The data is', form.cleaned_data.get('my_text'))
#
#    contex = {'form': form}
#    return render(request, 'index.html')

@method_decorator(name='dispatch', decorator=measure_execution_time) # the pythonic way
class Dashboard(ListView):
    model = Post
    template_name = 'posts/dashboard.html'
    paginate_by = 4
    query_param = 'query'
    form_class = SearchForm

#    @measure_execution_time # overriding the dispatch method not good pratice
#    def dispatch(self, request, *args, **kwargs):
#        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        kwargs.update({
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, ""),
        })
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all()
        search_value = self.request.GET.get(self.query_param)

        if search_value:
            queryset = queryset.filter(
                Q(title__icontains=search_value)
                    |
                Q(content__icontains=search_value)
                    |
                Q(author__icontains=search_value)
            )
        return queryset


#def dashboard(request):
#    search_form = SearchForm(request.GET)
#    posts = Post.objects.all()

#    if request.method == "GET" and search_form.is_valid():
#        query = search_form.cleaned_data.get('query')
#        posts = posts.filter(
#            Q(title__icontains=query)
#            |
#            Q(content__icontains=query)
#            |
#            Q(author__icontains=query)
#        )

#    context = {
#        "posts": posts,
#        "search_form": search_form,
#    }

#    return render(request, 'posts/dashboard.html', context)

class CreatePost(TimeRestrictedMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/add-post.html'



#def add_post(request):
#    form = PostCreateForm(request.POST or None, request.FILES or None)
#    if request.method == "POST" and form.is_valid():
#        form.save()
#        return redirect('dashboard')

#    context = {
#        "form": form,
#    }

#   return render(request, 'posts/add-post.html', context)


class EditPost(UpdateView):
    model = Post
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/edit-post.html'
#    form_class = PostEditForm      static way

    def get_form_class(self):
        if self.request.user.is_superuser:
            return modelform_factory(Post, fields='__all__')
        else:
            return modelform_factory(Post, fields=('content',),)


#def edit_post(request, pk: int):
#    post = Post.objects.get(pk=pk)
#   form = PostEditForm(request.POST or None, instance=post)
#    if request.user.is_superuser:

#        PostEditForm = modelform_factory(Post, fields='__all__')
#    else:
#        PostEditForm = modelform_factory(Post, fields=('content',),)

#    form = PostEditForm(request.POST or None, instance=post)

#    if request.method == "POST" and form.is_valid():
#        form.save()
#        return redirect('dashboard')

#    context = {
#        "form": form,
#    }

#    return render(request, 'posts/edit-post.html', context)


class PostDetails(DetailView, FormMixin):
    model = Post
    template_name = 'posts/post-details.html'
    form_class = CommentFormSet

    def get_context_data(self, **kwargs):
        kwargs.update({
            "formset": self.form_class(),
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={ 'pk': self.kwargs.get(self.pk_url_kwarg)})

#    def get_form_class(self):
#        return CommentFormSet

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form_set = self.get_form_class()(request.POST)

        if comment_form_set.is_valid():
            for form in comment_form_set:
                comment = form.save(commit=False)
                comment.author = request.user.username
                comment.post = self.object
                comment.save()
            return self.form_valid(comment_form_set)

#def post_details(request, pk: int):
#    post = Post.objects.get(pk=pk)
#    comment_form_set = CommentFormSet(request.POST or None)

#    if request.method == "POST" and comment_form_set.is_valid():
#        for form in comment_form_set:
#            comment = form.save(commit=False)
#            comment.author = request.user.username
#            comment.post = post
#            comment.save()
#            return redirect('post-details', pk=post.pk)

#    context = {
#        "post": post,
#        "formset": comment_form_set,
#    }

#    return render(request, 'posts/post-details.html', context)


class DeletePost(DeleteView, FormView):
    model = Post
    form_class = PostDeleteForm
    template_name = 'posts/delete-post.html'
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        post = self.model.objects.get(pk=pk)
        return post.__dict__


#   def delete_post(request, pk: int):
#    post = Post.objects.get(pk=pk)
#    form = PostDeleteForm(instance=post)

#    if request.method == "POST":
#        post.delete()
#        return redirect('dashboard')

#    context = {
#        "form": form,
#    }

#    return render(request, 'posts/delete-post.html', context)




#    if request.method == "POST":
#        return redirect('index')


#    context = {
#       "personal_info": {"first_name": "plamen",
#            "last_name": "STANCHEV",
#           "alias": "chicko trevichko"
#        },
#       "current_time":datetime.now(),
#       "is_hungry": None,
#       "favourite_songs": ["Dr.Dre - Still Dre", "2pac - Hit'em Up", "Eminem - Lose yourself", "Wu-Tang Clan - Protect ya neck"]
#   }

#    context = {
#        "posts": [
#            {
#                "title": "How to work with templates?",
#                "author": "Diyan Kalaydzhiev",
#                "content": "**Hey** how <i>can</i> i work with templates in Django? I am really bad at this. My first time using them.",
#                "created_at": datetime.now(),
#            },
#            {
#                "title": "was dido lecture good?",
#                "author": "Anonymous",
#                "content": "Should i watch it?",
#                "created_at": datetime.now(),
#            },
#            {
#                "title": "What is the next lecture?",
#                "author": "",
#                "content": "Hey guys i have no idea, pls answer!!!",
#                "created_at": datetime.now(),
#            },
#        ],
#    }
#    return render(request, 'base.html' , context)

class MyRedirectView(RedirectView):
#    url = 'http://localhost:8000/dashboard'
#    pattern_name = 'dashboard'
#    both static way

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard') + "?query = Django" # dynamic way