import django_filters
from .models import Board, NoticeBoard



class BoardFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Search Title')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains', label='Search Content')
    username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains', label='Search Username')

    class Meta:
        model = Board
        fields = ['title', 'content', 'username']


class NoticeBoardFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Search Title')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains', label='Search Content')
    username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains', label='Search Username')

    class Meta:
        model = NoticeBoard
        fields = ['title', 'content', 'username']