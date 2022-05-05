from django import forms
from .models import PostModel

class AddPostForm(forms.ModelForm):
    file = forms.FileField(required=False,widget=forms.FileInput(attrs={'class':'custom-file-input','id':'exampleInputFile'}))
    class Meta:
        model = PostModel
        fields = ('title',)
        
    def __init__(self,*args,**kwargs):
        super(AddPostForm,self).__init__(*args,**kwargs)
        
        self.fields['title'].widget.attrs = {'class':'form-control'}