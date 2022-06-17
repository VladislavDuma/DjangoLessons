from django.shortcuts import render, \
    get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator

from .models import Post
from .forms import PostForm, PostDeleteForm

from taggit.models import Tag


def home(request, tag=None):
    tag_obj = None

    if not tag:
        posts = Post.objects.all()
    else:
        tag_obj = get_object_or_404(Tag, slug=tag)
        posts = Post.objects.filter(tags__in=[tag_obj])

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    result = render(
        request,
        'home.html',
        {
            'section': 'home',
            'posts': posts,
            'tag': tag_obj
        }
    )
    return result


def detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    result = render(
        request,
        'blog/detail.html',
        {
            'section': 'blog_detail',
            'post': post
        }
    )
    return result


@permission_required('blog.add_post', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST,
                        request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    result = render(
        request,
        'blog/create.html',
        {
            'section': 'blog_create',
            'form': form,
        }
    )
    return result


@permission_required('blog.change_post', raise_exception=True)
def edit(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST,
                        request.FILES,
                        instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    result = render(
        request,
        'blog/edit.html',
        {
            'section': 'blog_edit',
            'form': form,
            'post': post,
        }
    )
    return result


@permission_required('blog.delete_post', raise_exception=True)
def delete(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            post.delete()
            return redirect('home')
    else:
        form = PostDeleteForm(instance=post)
    result = render(
        request,
        'blog/delete.html',
        {
            'section': 'blog_delete',
            'form': form,
            'post': post,
        }
    )
    return result
