from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationFormExtended(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['groups'].required = True

    def save(self, commit=True):
        user = super(UserCreationFormExtended, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        # import ipdb; ipdb.set_trace()
        if commit:
            user.save()
            user.groups = self.cleaned_data['groups']
            user.save()
        return user

    class Meta():

        model = User
        fields = ('username', 'password1', 'password2', 'groups')
