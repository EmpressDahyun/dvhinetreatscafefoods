from django.contrib.auth import password_validation
from store.models import DeliveryInformation, OrderRequest, Reservation
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = DeliveryInformation
        fields = ['recipient_name','phone_number','telephone_number','barangay','landmark','street_name','city']
        widgets = {
        'recipient_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Juan Dela Cruz'}), 
        'phone_number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}), 
        'telephone_number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telephone Number'}),
        'barangay':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ex. Cabatangan'}),  
        'landmark':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ex. Cabatangan Elementary School'}), 
        'street_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ex. Sitio Lumbang Road'}),
        'city':forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'})}

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'auto-focus':True, 'class':'form-control', 'placeholder':'Current Password'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'Confirm Password'}))

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['phone_number', 'telephone_number','pax', 'event_name','event_type','event_time','event_time_end','event_date','remarks']
        widgets = {'pax':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Number of Guest'}), 
        'phone_number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}), 
        'telephone_number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telephone Number'}),
        'event_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ex. Juan Dela Cruz 30th Birthday'}), 
        'event_type':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ex. Birthday'}),
        'event_time':forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
        'event_time_end':forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
        'event_date':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        'remarks':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Please list the foods that you want to reserve in this box, or Additional Request, Suggestions, Notes.'}),
        }

class OrderSlipForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = ['invoice_no','file_upload']