from django import forms
from django.contrib.auth import get_user_model
from .models import Wall,Post, Comment,Theme,Person

class FindForm(forms.Form):
    name=forms.CharField(required=False, widget=forms.TextInput(attrs={'title':'qq','size':40,'name':'qq'}))


class Registration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email','last_name','first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=('message',)
        widgets={
            'message': forms.Textarea(attrs={'cols':50,'rows':3})
                 }

class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=('message','title')
    #def __init__(self):
    #    self.fields['person'].queryset=Person.objects.filter(pk=1)
    #    self.fields['Wall'].queryset=Wall.objects.filter(pk=1)
class PostFormSave(forms.ModelForm):
    class Meta:
        model=Post
        fields=('message','title')

    def __init__(self,person_id, wall_id,*args,**kwargs):
        super(PostFormSave,self).__init__(*args,**kwargs)
        self.fields['person'].queryset=Person.objects.filter(pk=person_id)
        print(self.fields['person'])
        self.fields['Wall'].queryset=Wall.objects.filter(pk=wall_id)





