from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

class RoomForm(ModelForm):
    
    class  Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']


class UserForm(ModelForm):

    class Meta:
        model = User
        fields  = ['avatar','name','username', 'email','bio',]


        #           <div class="form__group">
        #     <label for="{{ field.auto_id }}">{{field.label}}</label>
        #     <div class="avatar avatar--large">
        #       <img class="" src="{{field.initial.url}}" />
        #     </div>
        #   </div>