from rest_framework import routers

from .views import ProfileViewSet

# Создаем router и регистрируем наш ViewSet
router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)

# URLs настраиваются автоматически роутером
urlpatterns = router.urls
