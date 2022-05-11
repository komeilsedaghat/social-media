from django import forms
from .models import CommentModel, PostModel

class AddPostForm(forms.ModelForm):
    file = forms.FileField(required=False,widget=forms.FileInput(attrs={'class':'custom-file-input','id':'exampleInputFile'}))
    class Meta:
        model = PostModel
        fields = ('title',)
        
    def __init__(self,*args,**kwargs):
        super(AddPostForm,self).__init__(*args,**kwargs)
        
        self.fields['title'].widget.attrs = {'class':'form-control'}



class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('comment',)
        
    def __init__(self,*args,**kwargs):
        super(CommentForm,self).__init__(*args,**kwargs)
        
        self.fields['comment'].widget.attrs = {'class':'form-control','placeholder':'Comment...'}



class CommentMessagesForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('status',)
        
    def __init__(self,*args,**kwargs):
        super(CommentMessagesForm,self).__init__(*args,**kwargs)
        
        self.fields['status'].widget.attrs = {'class':'form-control'}

