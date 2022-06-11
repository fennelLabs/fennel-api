from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from graphene_django.views import GraphQLView

from main.schema import schema
from main import views

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet)
router.register(r'identities', views.IdentityViewSet)
router.register(r'message_encryption_indicators', views.MessageEncryptionIndicatorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
