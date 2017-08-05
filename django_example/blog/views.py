import datetime
from django.http import HttpResponse
from django.urls import Resolver404
from blog.auth import authorize
from blog.models import Article


def dispatch(request, *args, **kwargs):
    if request.method == 'GET':
        return index(request, *args, **kwargs)
    elif request.method == "POST":
        return create(request, *args, **kwargs)
    else:
        raise Resolver404


def item_dispatch(request, *args, **kwargs):
    if request.method == 'GET':
        return show(request, *args, **kwargs)
    elif request.method == "PUT":
        return update(request, *args, **kwargs)
    elif request.method == "DELETE":
        return delete(request, *args, **kwargs)
    else:
        raise Resolver404


def index(request):
    authorize(request.user, 'read', Article)
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def create(request):
    authorize(request.user, 'create', Article)
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def show(request, article_id):
    article = Article.objects.get(pk=article_id)
    authorize(request.user, 'read', article)
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def update(request, article_id):
    article = Article.objects.get(pk=article_id)
    authorize(request.user, 'update', article)
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def delete(request, article_id):
    article = Article.objects.get(pk=article_id)
    authorize(request.user, 'delete', article)
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
