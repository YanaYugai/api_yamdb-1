from django_filters import FilterSet, CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр для произведений."""
    category = CharFilter(field_name='category',
                          lookup_expr='icontains')
    genre = CharFilter(field_name='genre',
                       lookup_expr='icontains')
    name = CharFilter(field_name='name',
                      lookup_expr='icontains')
    year = CharFilter(field_name='year',
                      lookup_expr='icontains')

    class Meta:
        class Meta:
            model = Title
            fields = '__all__'
