from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View

# from my models
from shop.models import Item, OrderItem, Order, BillingAddress

# time zone for when the item was added
from django.utils import timezone

# messages are like giving extra content
from django.contrib import messages

# get errors
from django.core.exceptions import ObjectDoesNotExist

# get forms
from .forms import CheckoutForm


# shop stuff
class CheckoutView(View):
    ''' user checkout '''
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        context = {
            'page': 'shop',
            'form': form,
        }
        return render(self.request, 'shop/checkout.html', context)

    def post(self, *args, **kwargs):
        ''' post data '''
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                # gets cleaned data
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_address = form.cleaned_data.get('zip_address')
                # TODO: Later
                # billing_address = form.cleaned_data.get('billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_options = form.cleaned_data.get('payment_options')

                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_address=zip_address,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                # TODO: redirect to payment
                return redirect('checkout')
            else:
                # form is not valid and return form with error
                args = {'form': form}
                return render(self.request, 'shop/checkout.html', args)
        except ObjectDoesNotExist:
            extra_context = {'extra_context':{'message':'True','message_title':'Warning: ','message_text':'You do not have an active order'}}
            return render(self.request, 'shop/home.html', extra_context)


# views
class ItemsView(ListView):
    ''' displays all items in shop '''
    model = Item
    # how many items per page
    paginate_by = 12
    template_name = 'shop/shop.html'


class ItemDetailView(DetailView):
    ''' show product detail '''
    model = Item
    template_name = 'shop/product.html'


class OrderSummaryView(View):
    ''' summarizes user's order '''
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'shop/cart.html', context)
        except ObjectDoesNotExist:
            extra_context = {'extra_context':{'message':'True','message_title':'Warning: ','message_text':'You have no items in your cart'}}
            return render(self.request, 'shop/home.html', extra_context)
        except Exception:
            extra_context = {'extra_context':{'message':'True','message_title':'Warning: ','message_text':e}}
            return render(self.request, 'shop/home.html', extra_context)


# add/remove from cart
@login_required
def add_to_cart(request, slug):
    ''' add item to cart '''
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    # get requested order
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # if order exists
    if order_qs.exists():
        order = order_qs[0]
        # checks if order is in the order
        if order.items.filter(item__slug=item.slug).exists():
            # if user has item, add another one of that item
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "You added another one of this item to your cart")
            return redirect("product", slug=slug)
        else:
            # else add 1 to that order
            messages.success(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect("product", slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.success(request, "This item was added to your cart")
        return redirect("product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    ''' removes an item from cart '''
    # get the item
    item = get_object_or_404(Item, slug=slug)

    # get requested order
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # if order exists
    if order_qs.exists():
        order = order_qs[0]
        # checks if order is in the order
        if order.items.filter(item__slug=item.slug).exists():
            # get ordered item
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # removes 1 of the products if it exist
            order_item.quantity -= 1
            if order_item.quantity == 0:
                order.items.remove(order_item)
                messages.warning(request, "You don't have any of this item in your cart anymore")
                return redirect("product", slug=slug)

            order_item.save()
            messages.warning(request, "This item was removed from your cart")
            return redirect("product", slug=slug)
        else:
            messages.warning(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:

        # add message the user doesn't have an order yet
        messages.warning(request, "You do note have an active order")
        return redirect("product", slug=slug)


# add/remove from cart from cart
@login_required
def add_single_to_cart(request, slug):
    ''' add item to cart '''
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    # get requested order
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # if order exists
    if order_qs.exists():
        order = order_qs[0]
        # checks if order is in the order
        if order.items.filter(item__slug=item.slug).exists():
            # if user has item, add another one of that item
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "You added another one of this item to your cart")
            return redirect("cart")
        else:
            # else add 1 to that order
            messages.success(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect("cart")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.success(request, "This item was added to your cart")
        return redirect("cart")

@login_required
def remove_single_from_cart(request, slug):
    ''' removes an item from cart '''
    # get the item
    item = get_object_or_404(Item, slug=slug)

    # get requested order
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # if order exists
    if order_qs.exists():
        order = order_qs[0]
        # checks if order is in the order
        if order.items.filter(item__slug=item.slug).exists():
            # get ordered item
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # removes 1 of the products if it exist
            order_item.quantity -= 1

            if order_item.quantity == 0:
                order_item.save()
                order.items.remove(order_item)
                messages.warning(request, "You don't have any of this item in your cart anymore")
                return redirect("cart")

            order_item.save()
            messages.warning(request, "This item was removed from your cart")
            return redirect("cart")
        else:
            messages.warning(request, "This item was not in your cart")
            return redirect("cart")
    else:

        # add message the user doesn't have an order yet
        messages.warning(request, "You do note have an active order")
        return redirect("cart")


@login_required
def remove_all_from_cart(request, slug):
    ''' removes all of this item from cart '''
    # get the item
    item = get_object_or_404(Item, slug=slug)

    # get requested order
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # if order exists
    if order_qs.exists():
        order = order_qs[0]
        # checks if order is in the order
        if order.items.filter(item__slug=item.slug).exists():
            # get ordered item
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # removes all of the products if it exist
            order_item.quantity = 0
            order.items.remove(order_item)
            messages.warning(request, "You don't have any of this item in your cart anymore")
            return redirect("cart")

        else:
            messages.warning(request, "This item was not in your cart")
            return redirect("cart")
    else:

        # add message the user doesn't have an order yet
        messages.warning(request, "You do note have an active order")
        return redirect("cart")


# home page
def home(request):
    ''' homepage '''
    keywords = {"page": "home"}
    return render(request, 'shop/home.html', keywords)


def home_redirect(request):
    ''' redirect to home '''
    return redirect('home')
