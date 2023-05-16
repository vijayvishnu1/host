
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from .models import *
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)



class ClientSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={'class': 'form-control','id':'email_id','onkeyup':"email_validate()",}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'onkeyup':"vfname()",'id':'fid',}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={ 'class': 'form-control','id':'lid','onkeyup':"lname()",}))
    phone_number = forms.CharField(max_length=10,widget=forms.TextInput(attrs={ 'class': 'form-control','id':'phid','onkeyup':"phone()",}))
    address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','id':'addressid','onkeyup':"address()",}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email','first_name','last_name','phone_number','address', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','id':'user_id','onkeyup':"validate_username()",}),
            #'email': forms.EmailInput(attrs={'class': 'form-control','id':'email_id','onkeyup':"email_validate()",}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id':'fid',}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address','onkeyup':"address()"}),
            'password1':forms.PasswordInput(attrs={'class':'form-control','id':'password1','onkeyup':"pass1Validate()"}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control','id':'password2','onkeyup':"pass2Validate()"}),

            #'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth'}),
            #'gender': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter Gender'}),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        #user.email = self.cleaned_data('email')
        user.save()
        client = Client.objects.create(user=user)
        client.phone_number = self.cleaned_data.get('phone_number')
        client.address = self.cleaned_data.get('address')
        client.save()
        return user


class AdvocateSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'onkeyup':"vfname()",'id':'fid',}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={ 'class': 'form-control','id':'lid','onkeyup':"lname()",}))
    license_number = forms.CharField(required=True,widget=forms.TextInput(attrs={ 'class': 'form-control','id':'licid','onkeyup':"license()",}))
    office_address = forms.CharField(required=True,widget=forms.TextInput(attrs={ 'class': 'form-control','id':'addressid','onkeyup':"address()",}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'license_number', 'office_address', 'password1', 'password2']
        exclude =['phone_number','experience','specifications','languages','description','pimage','dob','court']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'user_id', 'onkeyup': "validate_username()", }),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email_id', 'onkeyup': "email_validate()", }),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1', 'onkeyup': "pass1()"}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2', 'onkeyup': "pass2()"}),

        }


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_advocate = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        advocate = Advocate.objects.create(user=user)
        advocate.license_number = self.cleaned_data.get('license_number')
        advocate.office_address = self.cleaned_data.get('office_address')
        advocate.save()
        return user

class ClientcaseForm(forms.ModelForm):
        title = forms.CharField()
        description = forms.Textarea()
        proof = forms.FileField()
        defendant_name = forms.CharField()
        case_type = forms.ChoiceField(choices=Clientcase.type)
        defendant_address = forms.CharField()
        class Meta:
         model = Clientcase
         exclude = ['user','is_requested','is_pending','is_accepted','is_rejected','is_notrequested']



class ClientprofileForm(forms.ModelForm):
    house_name=forms.CharField()
    city = models.CharField()
    district = models.CharField()
    state = models.CharField()
    postoffice = models.CharField()
    picode = models.CharField()
    pimage = models.ImageField()
    date_of_birth = models.DateField(default=None)
    class Meta:
        model = Clientprofiles
        exclude =['user','adult']
class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Clientfeedback
        exclude = ['user']

class ContactusForm(forms.ModelForm):
    class Meta:
       model= contactus
       fields = '__all__'

# class ReviewForm(forms.ModelForm):
#     rating = forms.ChoiceField()
#     class Meta:
#         model = Review
#         fields = ['rating', 'description']

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        (1, mark_safe('&#9733;')),
        (2, mark_safe('&#9733;&#9733;')),
        (3, mark_safe('&#9733;&#9733;&#9733;')),
        (4, mark_safe('&#9733;&#9733;&#9733;&#9733;')),
        (5, mark_safe('&#9733;&#9733;&#9733;&#9733;&#9733;')),
    )

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select form-select-lg mb-3',
        'aria-label': 'Rating',
        'style': 'color: gold;'
    }))

    class Meta:
        model = Review
        fields = ['rating', 'comment']




#(1, mark_safe('&#9733;')),


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@---ADVOCATE-----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#--------------advocate profile update

class Advocateprofileupdate(forms.ModelForm):
    class Meta:
        model= Advocate
        fields=['phone_number','experience','specifications','languages','description','pimage','dob','court']

class ScheduleForm(forms.ModelForm):
    class Meta:
       model= Schedule
       fields = ['date','start_time','end_time','description']

class CaseAssignmentForm(forms.ModelForm):
    case = forms.ModelChoiceField(queryset=Clientcase.objects.all())
    class Meta:
        model = CaseAssignment
        exclude = ['requested_by','advocate','assigned_at']

# class CaseForm(forms.ModelForm):
#     judges = forms.MultipleChoiceField(choices=[(judge.id, str(judge)) for judge in Judge.objects.all()])
#
#     class Meta:
#         model = Case
#         fields = ['title', 'description', 'date_filed', 'court', 'cnr', 'status', 'outcome', 'judges']