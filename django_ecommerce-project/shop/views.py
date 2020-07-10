from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View

# get settings
from django.conf import settings

# from my models
from shop.models import Item, OrderItem, Order, BillingAddress, Payment

# time zone for when the item was added
from django.utils import timezone

# messages are like giving extra content
from django.contrib import messages

# get errors
from django.core.exceptions import ObjectDoesNotExist

# get forms
from .forms import CheckoutForm

# stripe
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


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
                return redirect('payment', payment_options='stripe')
            else:
                # form is not valid and return form with error
                args = {'form': form}
                return render(self.request, 'shop/checkout.html', args)
        except ObjectDoesNotExist:
            extra_context = {'extra_context':{'message':'True','message_title':'Warning: ','message_text':'You do not have an active order'}}
            return render(self.request, 'shop/home.html', extra_context)


class PaymentView(View):
    ''' view for actually paying '''
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)

        context = {
            'object': order
        }
        return render(self.request, "shop/payment.html", context)

    def post(self, *args, **kwargs):
        ''' what happens when payment view is posted '''
        token = self.request.POST.get('stripeToken')
        order = Order.objects.get(user=self.request.user, ordered=False)

        amount = int(order.get_final_price() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = int(order.get_final_price())
            payment.save()

            # assign the payment to the order
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was successful!")
            return redirect("home")

        except stripe.error.CardError as e:
            body = e.json_body
        #     err = body.get('error', {})
        #     messages.warning(self.request, f"{err.get('message')}")
        #     return redirect("home")

        # except stripe.error.RateLimitError as e:
        #     # Too many requests made to the API too quickly
        #     messages.warning(self.request, "Rate limit error")
        #     return redirect("home")

        # except stripe.error.InvalidRequestError as e:
        #     # Invalid parameters were supplied to Stripe's API
        #     messages.warning(self.request, "Invalid parameters")
        #     return redirect("home")

        # except stripe.error.AuthenticationError as e:
        #     # Authentication with Stripe's API failed
        #     # (maybe you changed API keys recently)
        #     messages.warning(self.request, "Not authenticated")
        #     return redirect("home")

        # except stripe.error.APIConnectionError as e:
        #     # Network communication with Stripe failed
        #     messages.warning(self.request, "Network error")
        #     return redirect("home")

        # except stripe.error.StripeError as e:
        #     # Display a very generic error to the user, and maybe send
        #     # yourself an email
        #     messages.warning(
        #         self.request, "Something went wrong. You were not charged. Please try again.")
        #     return redirect("home")

        # except Exception as e:
        #     # send an email to ourselves
        #     messages.warning(
        #         self.request, "A serious error occurred. We have been notified.")
        #     return redirect("home")


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
