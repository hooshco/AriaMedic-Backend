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
    path('panel',views.dashboard,name="dashboard"),
    path('panel/state',views.state,name="state"),
    path('panel/state/update/<int:id>',views.update_state,name="update_state"),
    path('panel/state/delete/<int:id>',views.delete_state,name="delete_state"),

    path('panel/major',views.major,name="major"),
    path('panel/major/update/<int:id>',views.update_major,name="update_major"),
    path('panel/major/delete/<int:id>',views.delete_major,name="delete_major"),

    path('panel/tag',views.tag,name="tag"),
    path('panel/tag/update/<int:id>',views.update_tag,name="update_tag"),
    path('panel/tag/delete/<int:id>',views.delete_tag,name="delete_tag"),

    path('panel/publisher',views.publisher,name="publisher"),
    path('panel/publisher/update/<int:id>',views.update_publisher,name="update_publisher"),
    path('panel/publisher/delete/<int:id>',views.delete_publisher,name="delete_publisher"),

    path('panel/discount',views.discount,name="discount"),
    path('panel/discount/update/<int:id>',views.update_discount,name="update_discount"),
    path('panel/discount/delete/<int:id>',views.delete_discount,name="delete_discount"),

    path('panel/category',views.category,name="category"),
    path('panel/category/update/<int:id>',views.update_category,name="update_category"),
    path('panel/category/delete/<int:id>',views.delete_category,name="delete_category"),

    path('panel/products',views.products,name="product"),
    path('panel/products/insert',views.insert_products,name="insert_product"),
    path('panel/product/update/<int:id>',views.update_product,name="update_product"),
    path('panel/product/delete/<int:id>',views.delete_product,name="delete_product"),

    path('panel/video',views.video,name="video"),
    path('panel/video/update/<int:id>',views.update_video,name="update_video"),
    path('panel/video/delete/<int:id>',views.delete_video,name="delete_video"),

    path('panel/sound',views.sound,name="sound"),
    path('panel/sound/update/<int:id>',views.update_sound,name="update_sound"),
    path('panel/sound/delete/<int:id>',views.delete_sound,name="delete_sound"),

    path('panel/book',views.book,name="book"),
    path('panel/book/update/<int:id>',views.update_book,name="update_book"),
    path('panel/book/delete/<int:id>',views.delete_book,name="delete_book"),

    path('panel/quize',views.quize,name="quize"),
    path('panel/quize/update/<int:id>',views.update_quize,name="update_quize"),
    path('panel/quize/delete/<int:id>',views.delete_quize,name="delete_quize"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)