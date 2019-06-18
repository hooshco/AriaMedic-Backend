from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Pastebin API')


urlpatterns = [

    path('register',views.Register,name="Register"),
    path('login',views.Login,name="Login"),
    path('logout',views.Login,name="Logout"),

    path('state',views.state,name="state"),
    path('state/insert',views.state,name="insert_state"),
    path('state/update/<int:id>',views.update_state,name="update_state"),
    path('state/delete<int:id>',views.delete_state,name="delete_state"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)