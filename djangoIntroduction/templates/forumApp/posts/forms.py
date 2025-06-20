from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from posts.mixins import ReadOnlyFieldsMixin
from posts.models import Post, Comment


class PostBaseForm(forms.ModelForm):
#    content2 = forms.CharField(max_length = 10, error_messages={
#        'max_length':' your message is too long',
#    })
    class Meta:
        model = Post
        fields = '__all__'

        widgets = {
            'language': forms.RadioSelect(
                attrs={'class': 'radio-select'},
            )
        }
        error_messages = {
            'author': {
                'max_length': 'The author\'s name is too long.',
            }
        }

    def clean_author(self):
        author = self.cleaned_data.get('author')

        if not author.isalpha():
            raise ValidationError('The author\'s name should only contain letters.')

        return author


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title.lower() in content.lower():
            raise ValidationError("The post title should not be included in the content.")

        return cleaned_data

    def save(self, commit=True):
        post = super().save(commit=False)
        post.author = post.author.capitalize()
        if commit:
            post.save()
        return post


class PostCreateForm(PostBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'


class PostEditForm(PostBaseForm):
    pass


class PostDeleteForm(ReadOnlyFieldsMixin, PostBaseForm):
    pass


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search for posts...'},
        )
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        labels = {
            'content':  '',
        }
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your comment...',
                }
            )
        }

CommentFormSet = formset_factory(CommentForm, extra=1)









#class MyForm(forms.Form):
#    CHOICES = [('diplomatic option', 'Diplomatic option'), ('nuclear option', 'Nuclear option')]

#    my_name = forms.CharField(max_length=10,
#                              required=False,
#                              initial='type your name here',
#                              label='Name',
#                              help_text='Enter your name',
#                              widget=forms.TextInput(attrs={'cols': 80, 'rows': 8, 'placeholder': 'Enter your name', 'class': 'form-control'})
#                              )
#    my_password = forms.CharField(max_length=10,widget=forms.PasswordInput,)
#    my_text = forms.CharField(widget=forms.Textarea)
#    my_number = forms.CharField(widget=forms.NumberInput)
#    my_other_number = forms.IntegerField(widget=forms.NumberInput)
#    radio = forms.ChoiceField(choices=CHOICES,
#                              widget=forms.RadioSelect)
#    multiple_select = forms.MultipleChoiceField(choices=CHOICES,
#                                                widget=forms.CheckboxSelectMultiple)
#    date = forms.DateField(widget=forms.SelectDateWidget)

