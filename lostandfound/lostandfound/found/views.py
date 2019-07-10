from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.urls import reverse
# Create your views here.
from .models import Found
from products.models import Lost_Product,ProductImage
def view(request):
    found=Found.objects.all()[0]
    context={"found":found}
    template="found/view.html"

    return render(request,template,context)

def update_found(request,id=None):
    found=Found.objects.all()[0]
    product=Lost_Product.objects.get(id=id)
    if not product in found.products.all():
        found.products.add(product)
        product.active=False
        product.save()

    else:
        found.products.remove(product)
        product.active=True
        product.save()
    found.total=len(found.products.all())
    found.save()
    return HttpResponseRedirect("/lostproducts")
