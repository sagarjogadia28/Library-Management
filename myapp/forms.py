from django import forms
from django.contrib.auth.forms import UserCreationForm

from myapp.models import Order, Review, Member


class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    name = forms.CharField(max_length=100, required=False, label="Your Name")
    category = forms.ChoiceField(widget=forms.RadioSelect, choices=CATEGORY_CHOICES, required=False,
                                 label="Select a category:")
    max_price = forms.DecimalField(label="Maximum Price", required=True, min_value=0)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {'book': forms.RadioSelect}
        labels = {'reviewer': u'Please enter a valid email',
                  'rating': u'Rating: An integer between 1 (worst) and 5 (best)'}

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError('You must enter a rating between 1 and 5!')
        return rating


class RegisterForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['username', 'password1', 'password2', 'profile_image', 'first_name', 'last_name', 'status', 'address',
                  'city', 'province', 'auto_renew']
