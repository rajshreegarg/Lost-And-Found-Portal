
from django.urls import path
from django.conf.urls.static import static


from django.conf import settings
from django.conf.urls import include, url
from products.views import lost_list,lost_detail,lost_update,lost_delete,lost_create
from found.views import update_found
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [

    url(r'^$',lost_list,name='lostproducts'),
    url(r'^create/$',lost_create,name='lostform'),
    url(r'^(?P<id>\d+)/$',lost_detail,name='single_product'),
    url(r'^(?P<id>\d+)/edit/$',lost_update,name='lost_update'),
    url(r'^(?P<id>\d+)/delete/$',lost_delete,name='lost_delete'),
    url(r'^(?P<id>\d+)/found/$',update_found,name='update_found'),






]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
