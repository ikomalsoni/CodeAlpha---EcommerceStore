from django.db.models import Q
from django.shortcuts import render,redirect
from .models import Product,Cart,Order

def home(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request, "store/index.html", {"products": products})
   
def cart(request):
    carts = Cart.objects.all()
    total = sum(item.product.price * item.quantity for item in carts)
    return render(request, "store/cart.html", {
        "carts": carts,
        "total": total
    })    
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    Cart.objects.create(product=product, quantity=1)
    return redirect("cart")
    
def product_detail(request , id):
    product = Product.objects.get(id=id) 
    return render(request,"store/product_detail.html",{"product": product})  

def checkout(request):
    carts = Cart.objects.all()
    total = sum(item.product.price * item.quantity for item in carts)

    if request.method == "POST":
        customer_name = request.POST["customer_name"]
        address = request.POST["address"]

        Order.objects.create(
            customer_name=customer_name,
            address=address,
            total_amount=total
        )

        carts.delete()
        return redirect("home")

    return render(request, "store/checkout.html", {"total": total})     
