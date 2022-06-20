# Create your views here.
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from musics.models import Music
from musics.serializers import MusicSerializer
from django_redis import get_redis_connection
import time

con = get_redis_connection("default")

# Create your views here.
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def list(self, request, **kwargs):
        if self.request.version == '1.0':
            if 'musics' in cache:
                # from cache get musics
                musics = cache.get('musics')
            else:
                musics = Music.objects.all()
                serializer = MusicSerializer(musics, many=True)
                musics = serializer.data
                # store data to cache
                cache.set('musics', musics, timeout=None)
        else:
            musics = Music.objects.all()
            serializer = MusicSerializer(musics, many=True)
            musics = serializer.data
        return Response(musics, status=status.HTTP_200_OK)

    def list_lock(self, request, **kwargs):
        if self.request.version == '1.0':
            if 'musics' in cache:
                # from cache get musics
                musics = cache.get('musics')
            else:
                if con.set("my_key", "secret", nx=True, px=1000):
                    musics = Music.objects.all()
                    serializer = MusicSerializer(musics, many=True)
                    musics = serializer.data
                    cache.set('musics', musics, timeout=None)
                    print('store data to cache')
                else:
                    print("pending")
                    while 1:
                        time.sleep(0.5)
                        print('sleep')
                        if 'musics' in cache:
                            musics = cache.get('musics')
                            print('break')
                            break
        else:
            musics = Music.objects.all()
            serializer = MusicSerializer(musics, many=True)
            musics = serializer.data
        return Response(musics, status=status.HTTP_200_OK)
