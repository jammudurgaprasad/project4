#user:dp pw:12345
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.login_user,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout_user,name='logout'),
    path('home/',views.home,name='home'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('profile/',views.profile,name='profile'),
    path('orders/', views.orders_page, name='orders_page'),
    path('add_address',views.add_address,name='add_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('addresses/',views.addresses,name='addresses'),
    path('place_order/', views.place_order, name='place_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    path('about_us/',views.aboutus,name='aboutus'),
    path('menu_page/',views.menupage,name='menu'),
    path('offers_page/',views.offerspage,name='offers'),
    path('contactus_page/',views.contactus,name='contactus'),


    path('agent/',views.agentpage,name = 'agent'),
    path('deliver/<int:item_id>',views.delivered,name = 'deliver_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)