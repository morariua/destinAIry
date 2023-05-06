from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.view_UI, name='chatbotUI_for_TESTING'),
    path('api-key/', views.ApiKeyViewSet.api_key, name='view_create_api_key'),
    path('api/', views.view_API, name='chatbot_REST_API'),
    # the path below (which uses router) is an alternative method of making the create/delete API view.
    #path('api/', include(router.urls)),
    ## The path below is only used for curl requests.
    #path('api-keys/', views.ApiKeyViewSet.as_view({'post':'create'}), name='api_key_generate'),    
]
## add the following code to specify the custom 403 Forbidden handler:
from django.conf.urls import handler403
handler403 = views.error_403