from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('Tech', 'Technology'),
    ('Access', 'Accessories'),
    ('Trans', 'Transportation'),
    ('Misc', 'Other'),
)

LABEL_CHOICES = (
    ('N', 'New'),
    ('L', 'Limited'),
    ('S', 'Sold Out'),
)


class Item(models.Model):
    ''' the shopping item itself '''
    title = models.CharField(max_length=100)                                                        # name of product
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)                            # category
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True, null=True)            # label (optional)
    description = models.TextField(max_length=2500)                                                 # description of product
    image = models.ImageField(upload_to='images', blank=True, null=True)                            # product image
    price = models.DecimalField(max_digits=6, decimal_places=2, default=10)                         # price of item
    discounted_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)   # discounted price (optional)
    slug = models.SlugField()                                                                       # custom slag for item website

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return product website
        return reverse("product", kwargs={
            "slug": self.slug
        })

    def get_add_to_cart_url(self):
        ''' add item to cart '''
        return reverse("add_to_cart", kwargs={
            "slug": self.slug
        })

    def get_remove_from_cart_url(self):
        ''' removes item to cart '''
        return reverse("remove_from_cart", kwargs={
            "slug": self.slug
        })


class OrderItem(models.Model):
    ''' a list of ordered items '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)                                        # user
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)                             # list of items
    quantity = models.IntegerField(default=1)                                                       # how many items there are
    ordered = models.BooleanField(default=False)                                                    # is order

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    ''' the order itself '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)     # user
    items = models.ManyToManyField(OrderItem)                               # list of items belonging to user
    start_date = models.DateTimeField(auto_now_add=True)                    # start of first order
    ordered_date = models.DateTimeField()                                   # order date
    ordered = models.BooleanField(default=False)                            # is order

    def __str__(self):
        return self.user.username
