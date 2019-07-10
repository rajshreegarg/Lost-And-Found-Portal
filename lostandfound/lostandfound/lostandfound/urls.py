"""lostandfound URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import reverse_lazy

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from products.views import home,LandF
from products.views import all
from products.views import search
#from products.views import lost
from products.views import register
from products.views import view_profile, image_create
from products.views import edit_profile,change_password
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView,PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView,PasswordChangeView

from found.views import view,update_found

from django.contrib.auth import views as auth_views






from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    url(r'^$',home,name='home'),
    url(r'^image/$',image_create,name='imageform'),


    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^accounts/profile/$',RedirectView.as_view(url='/')),


    #url(r'^lostproducts/$',all,name='lostproducts'),

    #url(r'^lostproducts/(?P<slug>[\w-]+)/$',single,name='single_product'),

      #url(r'^admin1/', include('admin1.urls')),
    url(r'^LandF/$',LandF,name='LandF'),



    url(r'^s/$',search,name='search'),
    url(r'^found/$',view,name='found'),
    #url(r'^found/(?P<id>\d+)/$',update_found,name='update_found'),
    url(r'^lostproducts/',include("products.urls")),
#    url(r'^lostproducts/',include("products.urls" namespace='p')), so we will use it everywhere as p:single_product

    #url(r'^form/$',LostView.as_view(),name='lostform'),


    url(r'^login/$', auth_views.LoginView.as_view(template_name='products/login.html'),name='loginform'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='products/logout.html'),name='logoutform'),

    path('myadmin/', admin.site.urls,name='admin'),

    url(r'^register/$',register,name='register'),
    url(r'^profile/$',view_profile,name='view_profile'),
    url(r'^profile/edit/$',edit_profile,name='edit_profile'),
    url(r'^profile/password/$',change_password,name='change_password'),
    #url(r'^reset_password$',password_reset,name='reset_password'),
    #url(r'^reset_password/done$',password_reset_done,name='password_reset_done'),
    url(
        r"^profile/password-reset/$",
        PasswordResetView.as_view(),
        name="password_reset",
        ),
    url(
        r"^profile/password-reset/done/$",
    PasswordResetDoneView.as_view(),
        name="password_reset_done",
        ),
    url(
        r"^profile/password-reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
        ),

        url(
            r"^profile/password-reset/complete",
            PasswordResetCompleteView.as_view(),
            name="password_reset_complete",
            ),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),


]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
