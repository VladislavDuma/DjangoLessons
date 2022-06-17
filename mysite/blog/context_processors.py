from blog.models import Post


def latest_posts(request):
    posts = Post.objects.filter().order_by('-date')[:5]
    return {'latest_posts': posts}
