from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPageNumberPagination
from api.serializers import SubscribeSerializer, UserSerializer
from user.models import Subscription, User


class UserViewSet(UserViewSet):
    '''Вьюсет для представления пользователя и подписок.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        '''Подписаться на автора.'''
        serializer = SubscribeSerializer(
            get_object_or_404(User, id=self.kwargs.get('id')),
            data=request.data,
            context={"request": request})
        serializer.is_valid(raise_exception=True)
        Subscription.objects.create(user=request.user,
                                    author=get_object_or_404(
                                        User,
                                        id=self.kwargs.get('id')))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, **Kwargs):
        '''Удаление подписки на автора.'''
        get_object_or_404(
            Subscription,
            user=request.user,
            author=get_object_or_404(User, id=self.kwargs.get('id'))
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        '''Список подписок текущего пользователя.'''
        pages = self.paginate_queryset(User.objects.filter(
            subscribing__user=request.user))
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)
