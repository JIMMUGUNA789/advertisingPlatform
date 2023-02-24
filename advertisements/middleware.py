from re import compile
from .models import Ad

class AdImpressionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ad_image_pattern = compile(r'^/media/ads/(?P<ad_id>\d+)/(?P<filename>.+)$')

    def __call__(self, request):
        if request.path.startswith('/media/ads/'):
            match = self.ad_image_pattern.match(request.path)
            if match:
                ad_id = match.group('ad_id')
                ad = Ad.objects.get(pk=ad_id)
                ad.impressionsCount += 1
                ad.save()
        response = self.get_response(request)
        return response
