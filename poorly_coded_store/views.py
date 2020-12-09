from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    last = Order.objects.last()
    price = last.total_price
    total_orders = Order.objects.values_list('quantity_ordered', flat=True)
    total_order = sum(total_orders)
    total_prices = Order.objects.values_list('total_price', flat=True)
    total_price = sum(total_prices)
    context = {
        'orders': total_order,
        'total':  total_price,
        'bill': price,
    }
    return render(request, "store/checkout.html",context)

def purchase(request):
    if request.method == 'POST':
        this_product = Product.objects.filter(id=request.POST["id"])
        if not this_product:
            return redirect('/')
        else:
            quantity_from_form = int(request.POST["quantity"])
            total_charge = '%.2f' % (quantity_from_form * float(this_product[0].price))
    
            Order.objects.create(
                quantity_ordered=quantity_from_form, 
                total_price= total_charge,
                )
            return redirect("/checkout")
    else:
        return redirect("/")