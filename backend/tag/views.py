from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    '''Класс для тегов.'''
    queryset = Tag.objects.all()
    # serializer_class = TagSerializers
    # permission_classes
