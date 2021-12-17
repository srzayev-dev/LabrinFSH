from django import forms
from django.forms import widgets

from users.models import User
from core.models import Post,SharePost

class UploadFilesForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'title' : widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title of File'} ),
            'desc' : widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description of File'} ),
        }


    
class ShareFilesForm(forms.ModelForm):
    class Meta:
        model = SharePost
        fields = ('sharedUser', 'can_comment')

        widgets = {
            'can_comment' : widgets.RadioSelect(choices=((True, 'Yes'), (False, 'No'))),    
        }

    
    # def __init__(self, *args, **kwargs):
    #     super(ShareFilesForm, self).__init__(*args, **kwargs)
    #     """exclude the current user from the list of users"""
    #     self.fields['sharedUser'].queryset = User.objects.exclude(id=self.instance.user.id)