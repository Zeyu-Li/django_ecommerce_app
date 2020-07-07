from django import forms
# country
from django_countries.fields import CountryField

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(max_length=400)
    apartment_address = forms.CharField(max_length=400, required=False)
    country = CountryField(blank_label='(select country)').formfield()
    zip_address = forms.CharField(max_length=40)

    # options
    billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_options = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)