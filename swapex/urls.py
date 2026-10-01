"""
URL configuration for swapex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    """Root endpoint to confirm API is running"""
    return JsonResponse({
        'status': 'success',
        'message': 'SwapEx API is running',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api_auth': '/api/auth/',
            'api_products': '/api/products/',
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),  # Root URL
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/',include('products.urls')),
    # Make sure you don't have another path('api/token/', ...) here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
