from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from utils import get_all_properties

# @cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    # properties = Property.objects.all().values(
    #     'id', 'title', 'description', 'price', 'location', 'created_at'
    # )
    properties = get_all_properties()
    return JsonResponse(list(properties), safe=False)
