from django import forms
from mptt.forms import TreeNodeChoiceField

from .models import Comment


class CommentCreateForm(forms.ModelForm):
    """
    Форма добавления комментариев к изделяим
    """
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False



    class Meta:
        model = Comment
        fields = ('parent', 'content',)