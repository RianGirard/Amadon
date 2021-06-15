from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    quantity_from_form = int(request.POST["quantity"])
    instance = Product.objects.get(id=request.POST["id"])                           # instantiate the Product purchased; 
    total_charge = float(quantity_from_form * instance.price)
    display_charge = '{:,.2f}'.format(total_charge)
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    
    all_quantity = Order.objects.aggregate(Sum('quantity_ordered'))                 # "aggregate" object yields a dictionary; note also "Sum" imported above! 
    all_quantity_value = all_quantity.get('quantity_ordered__sum')                  # get the value from the dict key

    all_charges = Order.objects.aggregate(Sum('total_price'))                       # "aggregate" object yields a dictionary; note "Sum" imported above! 
    all_charges_value = all_charges.get('total_price__sum')                         # get the value from the key
    all_charges_value_format = '{:,.2f}'.format(all_charges_value)                  # format to a 2-decimal number for "cents"

    request.session['number'] = quantity_from_form                                  # use Session variables so that can redirect to new page after a POST form
    request.session['charge'] = display_charge
    request.session['sum_quantity'] = all_quantity_value
    request.session['sum_charge'] = all_charges_value_format

    # context = {
    #     "number": quantity_from_form,                                             # Context dict only good if you are "rendering"; not good on a POST form
    #     "charge": display_charge,
    #     "sum_quantity": all_quantity_value,
    #     "sum_charge": all_charges_value_format,
    # }
    return redirect('/summary')
    # return render(request, "store/checkout.html", context)

def summary(request):
    return render(request, "store/checkout.html" )