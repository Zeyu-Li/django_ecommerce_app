from django.shortcuts import render
from shop.models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone


def item_list(request):
    ''' list all item in shop '''
    context = {
        'items': Item.objects.all(),
        'page': 'shop'
    }
    return render(request, 'shop/shop.html', context)

def product(request):
    ''' product item page '''
    context = {
        'page': 'shop'
    }
    return render(request, 'shop/product.html', context)

@login_required
def checkout(request):
    ''' user checkout '''
    context = {
        'page': 'shop'
    }
    return render(request, 'shop/checkout.html', context)


class ItemsView(ListView):
    ''' displays all items in shop '''
    model = Item
    template_name = 'shop/shop.html'


class ItemDetailView(DetailView):
    ''' show product detail '''
    model = Item
    template_name = 'shop/product.html'


@login_required
def add_to_cart(request, slug):
    ''' add item to cart '''
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.items.create(item=item)
    order_qs = Order.items.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # checks if order is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("product", slug=slug)
        else:
            order.items.add(order_item)
            return redirect("product", slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.items.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("product", slug=slug)

# home page
def home(request):
    ''' homepage '''
    keywords = {"page": "home"}
    return render(request, 'shop/home.html', keywords)


def home_redirect(request):
    ''' redirect to home '''
    return redirect('home')
