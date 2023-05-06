from rest_framework import routers
from .views import ApiKeyViewSet
router = routers.DefaultRouter()
router.register(r'api-keys', ApiKeyViewSet) ## r'myapp-model-name'