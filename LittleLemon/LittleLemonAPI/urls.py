from django.urls import path,include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('menu-items', views.menu_items_view),
    path('menu-items/<int:id>', views.single_item_view),
    path('groups/manager/users', views.manager_view),
    path('groups/manager/users/<int:id>', views.single_manager_delete_view),
    path('groups/delivery-crew/users', views.delivery_view),
    path('groups/delivery-crew/users/<int:id>', views.single_delivery_delete_view),
    path('cart/menu-items', views.cart_view),
    path('orders', views.order_view),
    path('orders/<int:id>', views.single_order_view),
          
       
]
