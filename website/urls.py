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
    path('state/update/<int:id>',views.update_state,name="update_state"),
    path('state/delete<int:id>',views.delete_state,name="delete_state"),

    path('major',views.major,name="major"),
    path('major/update/<int:id>',views.update_major,name="update_major"),
    path('major/delete<int:id>',views.delete_major,name="delete_major"),

    path('tag',views.tag,name="tag"),
    path('tag/update/<int:id>',views.update_tag,name="update_tag"),
    path('tag/delete<int:id>',views.delete_tag,name="delete_tag"),

    path('publisher',views.publisher,name="publisher"),
    path('publisher/update/<int:id>',views.update_publisher,name="update_publisher"),
    path('publisher/delete<int:id>',views.delete_publisher,name="delete_publisher"),

    path('discount',views.discount,name="discount"),
    path('discount/update/<int:id>',views.update_discount,name="update_discount"),
    path('discount/delete<int:id>',views.delete_discount,name="delete_discount"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)