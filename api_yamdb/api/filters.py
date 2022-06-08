from django_filters import FilterSet, CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):

    genre = CharFilter(method='slug_filter')
    category = CharFilter(method='slug_filter')
    name = CharFilter(lookup_expr='icontains')

    def slug_filter(self, queryset, name, value):
        if name == 'genre':
            return queryset.filter(genre__slug=value)
        return queryset.filter(category__slug=value)

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')
