from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django_redis import get_redis_connection

from .models import Image

# Create your views here.

con = get_redis_connection("default")


def index(request):
    query = Image.objects.all()
    images_seq = [
        {'id': data.id,
         'Url': data.url,
         'CreateDate': data.create_date}
        for data in query
    ]

    cache.get_or_set('click', 0, timeout=None)
    total_views = cache.incr('click')

    rank = con.zrevrange(name='images', start=0, end=9, withscores=True, score_cast_func=int)
    rank_seq = [
        {"url": str(r[0], 'utf-8'),
         "value": r[1]}
        for r in rank
    ]

    return render(request, 'images/index.html', {
        'images': images_seq,
        'total_views': total_views,
        'ranks': rank_seq,
    })


def detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    total_views = con.zincrby(name='images', value=image.url)
    return render(request,
                  'images/detail.html', {
                      'image': image,
                      'total_views': int(total_views)
                  })
