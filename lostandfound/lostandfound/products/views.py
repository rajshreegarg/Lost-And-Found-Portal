
# Create your views here.
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm
from django.views import View
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import render,redirect,get_object_or_404
from products.forms import LostForm,ProductForm
from products.forms import RegisterationForm, EditProfileForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from found.models import Found

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Lost_Product, ProductImage

def search(request):
    if request.user.is_authenticated:
        queryset_list=Lost_Product.objects.all()
        try:
            query=request.GET.get('fieldkeywords')
        except:
            query=None
        if query:
            queryset_list=queryset_list.filter(
            Q(title__icontains=query)|
            Q(lostlocation__icontains=query)|
            Q(id__icontains=query)
                ).distinct()
        paginator = Paginator(queryset_list, 6) # Show 20 contacts per page
        page = request.GET.get('page')
        try:
            queryset=paginator.page(page)
        except PageNotAnInteger:
            queryset=paginator.page(1)#deliver first page
        except EmptyPage:
            queryset=paginator.page(paginator.num_pages)   #deliver last page
        context = {"query":query,"products":queryset,}

        template='products/results.html'
    else:
        queryset_list=Lost_Product.objects.filter(active=True)
        try:
            query=request.GET.get('fieldkeywords')
        except:
            query=None
        if query:
            queryset_list=queryset_list.filter(
            Q(title__icontains=query)|
            Q(lostlocation__icontains=query)|
            Q(id__icontains=query)
                ).distinct()
        paginator = Paginator(queryset_list, 6) # Show 20 contacts per page
        page = request.GET.get('page')
        try:
            queryset=paginator.page(page)
        except PageNotAnInteger:
            queryset=paginator.page(1)#deliver first page
        except EmptyPage:
            queryset=paginator.page(paginator.num_pages)   #deliver last page
        context = {"query":query,"products":queryset,}

        template='products/results_user.html'
    return render(request,template,context)



def home(request):
    if request.user.is_authenticated:
        context={'username_is':request.user}
    else:
        context={'username_is':request.user}

    #lostproducts=Lost_Product.objects.all()
    template='products/home.html'
    #context = {'lostproducts':lostproducts}
    return render(request,template,context)


def LandF(request, id=None):

    #lostproducts=Lost_Product.objects.all()
    template='products/L-FPortal.html'
    #context = {'lostproducts':lostproducts}
    return render(request,template)


def all(request):
    lostproducts=Lost_Product.objects.all()
    context = {'lostproducts':lostproducts}
    template='products/all.html'
    return render(request,template,context)

#def lost_detail(request,slug):
    #try:
#        product= Lost_Product.objects.get(slug=slug)
#        #images =  Lost_Product.productimage_set.all()
#        images= ProductImage.objects.filter(product=product)
#        context = {"product":product,"images":images}
#        template='products/single.html'
#        return render(request,template,context)
    #except:
        #raise Http404("Page does not exist")
def lost_detail(request,id=None):
    storage=messages.get_messages(request)
    product =  get_object_or_404(Lost_Product,id=id)
    images= ProductImage.objects.filter(product=product)
    context={"product":product,"images":images,'message':storage,}
    template='products/single.html'

    return render(request,template,context)

@login_required
def lost_update(request,id=None):
    instance = get_object_or_404(Lost_Product,id=id)
    if request.method=='POST':
        form=LostForm(request.POST , instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            messages.success(request,"Successfully Saved!")
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            messages.error(request,"Not Successfully Saved !")
    else:
        form=LostForm(instance=instance)
    context={"instance":instance,"form":form,}
    return render(request,"products/edit_lost_form.html",context)




@login_required
def lost_delete(request,id=None):
    instance = get_object_or_404(Lost_Product,id=id)
    instance.delete()
    messages.success(request,"Successfully Deleted!")
    return redirect('/lostproducts')


@login_required
def lost_create(request):
    if request.method == 'POST':
        form = LostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Successfully Created!")
            return HttpResponseRedirect('/lostproducts')
    else:
        form = LostForm()
    context = {'form': form}
    return render(request,"products/form.html", context)

def image_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Successfully Created!")
            return HttpResponseRedirect('/lostproducts')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request,"products/formimage.html", context)


def lost_list(request,id=None):
    storage=messages.get_messages(request)
    #try:

    if request.user.is_authenticated:
        template='products/lost.html'

        queryset_list=Lost_Product.objects.all()
        paginator = Paginator(queryset_list, 6) # Show 20 contacts per page
        page = request.GET.get('page')
        try:
            queryset=paginator.page(page)
        except PageNotAnInteger:
            queryset=paginator.page(1)#deliver first page
        except EmptyPage:
            queryset=paginator.page(paginator.num_pages)   #deliver last page
    else:
        template='products/lost_user.html'

        queryset_list=Lost_Product.objects.filter(active=True)
        paginator = Paginator(queryset_list, 6) # Show 6 contacts per page
        page = request.GET.get('page')
        try:
            queryset=paginator.page(page)
        except PageNotAnInteger:
            queryset=paginator.page(1)#deliver first page
        except EmptyPage:
            queryset=paginator.page(paginator.num_pages)   #deliver last page
    context = {"lostproducts":queryset,'message':storage,}

    return render(request,template,context)
    #except:
    #   raise Http404("Page does not exist")


#class login_view(request):
#    if request_method=='POST':
#        form=AuthenticationForm(data=request.POST)
#        if form.is_valid():
#            user = form.get_user()
#            login(request.user)
#            if 'next' in request.POST:
#                return redirect(request.POST.get('next'))
#            else:
#                return redirect("{% url 'home'%}")
#        else:
#            form=AuthenticationForm()
#        return render(request,'products/login.html',{'form':form})

@login_required
def register(request):

    if request.method=='POST':
        form=RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return redirect('/register')

    else:
        form=RegisterationForm()


        return render(request,"products/registerform.html",{'form':form})
@login_required
def view_profile(request):

    args={'user':request.user}
    return render(request,"products/profile.html",args)

@login_required
def edit_profile(request):
    if request.method=='POST':
        form=EditProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
        else:
            return redirect('/profile/edit')
    else:
        form=EditProfileForm(instance=request.user)
        args={'form':form}
        return render(request,"products/edit_profile.html",args)



@login_required
def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Your password has been reset.')
            update_session_auth_hash(request,form.user)
            return redirect('/profile')
        else:
            return redirect('/profile/password')
    else:
        form=PasswordChangeForm(user=request.user)

    args={'form':form }
    return render(request,'products/change_password.html',args)


#class edit_lostItem(View):
#    template_name="products/edit_lostform.html"
#    def get_object(self):
#        id=self.kwargs.get('id')
#        obj=None
#        if id is not None:
#            obj=get_object_or_404(Lost_Product,id=id)
#        return obj
#
#    def get(self,request,id=None,*args,**kwargs):
#        context={}
#        obj = self.get_object()
#        if obj is not None:
#            form = EditItemForm(instance=obj)
#            context['object']=obj
#            context['form']=form
#        return render(request,self.template_name,context)

#    def post(self,request,id=None,*args,**kwargs):
#        context={}
#        obj = self.get_object()
#        if obj is not None:
#            form=EditItemForm(request.POST,instance=obj)
#            if form.is_valid():
#                form.save()
#                return redirect('/lostproducts')
#            else:
#                return redirect('/lostproducts/edit')
#            context['object']=obj
#            context['form']=form
#        return render(request,self.template_name,context)
