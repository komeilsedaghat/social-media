from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import get_user_model
from .password_list import most_password

User = get_user_model()

class SigninUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields= ('username','password',)

    def __init__(self,*args,**kwargs):
        super(SigninUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Username Or Email '})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your Password'})



class SignupUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username','email','password1','password2','phone_number',)

    
    def __init__(self,*args,**kwargs):
        super(SignupUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs = {'class':'form-control', 'placeholder': 'Your Username'}
        self.fields['email'].widget.attrs= {'class':'form-control', 'placeholder': 'Your  Email' }
        self.fields['phone_number'].widget.attrs= {'class':'form-control', 'placeholder': 'Your Phone Number' }
        self.fields['password1'].widget.attrs= {'class':'form-control', 'placeholder': 'Your password' }
        self.fields['password2'].widget.attrs= {'class':'form-control', 'placeholder': 'Your Confirm Passwrod' }


    def clean_password2(self):
        p2 = self.cleaned_data['password2']
        p1 = self.cleaned_data['password1']
        if p2 != p1:
            raise forms.ValidationError('password not match')
        else:
            None

        if len(p2) < 5 :
            raise forms.ValidationError('you password is too short')
        else:
            None

        
        if p2 in most_password:
            raise forms.ValidationError("please Enter Stronger Passeord")

        


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('username','email','profile_img','phone_number','age','first_name','last_name',)

    def __init__(self,*args,**kwargs):
        super(ProfileUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs = {'class':'form-control', 'placeholder': 'Your Username'}
        self.fields['email'].widget.attrs= {'class':'form-control', 'placeholder': 'Your  Email' }
        self.fields['profile_img'].widget.attrs= {'class':'custom-file-input', 'placeholder': 'Your  profile photo','id':'exampleInputFile' }
        self.fields['phone_number'].widget.attrs= {'class':'form-control', 'placeholder': 'Your Phone Number' }
        self.fields['age'].widget.attrs= {'class':'form-control', 'placeholder': 'Your age' }
        self.fields['first_name'].widget.attrs= {'class':'form-control', 'placeholder': 'Your first name' }
        self.fields['last_name'].widget.attrs= {'class':'form-control', 'placeholder': 'Your last name' }
