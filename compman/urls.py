from django.urls import path
from rest_framework import routers

from compman.views import home_page_view, PlayerViewSet, TableViewSet, GameViewSet

router = routers.DefaultRouter()
router.register('players', PlayerViewSet, basename="players")
router.register('tables', TableViewSet, basename="tables")
router.register('games', GameViewSet, basename="games")

urlpatterns = [
                  path("hello", home_page_view, name="home"),
              ] + router.urls
