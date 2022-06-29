from django.shortcuts import render, \
    get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Post
from .forms import PostForm, PostDeleteForm
from .serializers import PostSerializer

from taggit.models import Tag


def home(request, tag=None):
    tag_obj = None

    if not tag:
        posts = Post.objects.all()
    else:
        tag_obj = get_object_or_404(Tag, slug=tag)
        posts = Post.objects.filter(tags__in=[tag_obj])

    paginator = Paginator(posts, 2)
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


# --------------------------------------------------------
#   API
# --------------------------------------------------------
@api_view(['GET', 'POST'])
@permission_required([IsAuthenticated])
def post_api_view(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        post_objects = Post.objects.all()
        result = paginator.paginate_queryset(post_objects, request)
        serializer = PostSerializer(result, many=True)
        # serializer = PostSerializer(Post.objects.all(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_required([IsAuthenticated])
def post_api_detail_view(request, pk=None):
    try:
        blog = Post.objects.get(pk=pk)
    except blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(blog)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(blog.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
