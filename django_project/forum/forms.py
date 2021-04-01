from django import forms
from django.forms import widgets
from forum import models as forum_model


class FileFieldForm(forms.Form):
    file_filed = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))


class ForumPostForm(forms.ModelForm):
    tag_help = forms.CharField(required=False)

    class Meta:
        model = forum_model.ForumPost
        fields = (
            "title",
            "content",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "cols": 50,
                    "rows": 1,
                    "placeholder": "제목을 입력해주세요",
                    "class": "appearance-none placeholder-gray-500 border border-gray-300 rounded-b-md focus:outline-none focus:border-indigo-500 focus:z-10",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "cols": 50,
                    "rows": 5,
                    "placeholder": "내용",
                    "class": "appearance-none placeholder-gray-500 border border-gray-300 rounded-b-md focus:outline-none focus:border-indigo-500 focus:z-10",
                    "style": "resize: none;",
                }
            ),
        }


class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = forum_model.ForumComment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "cols": 50,
                    "rows": 4,
                    "class": "p-2 appearance-none placeholder-gray-500 border border-gray-300 focus:outline-none focus:border-blue-500",
                    "style": "resize: none;",
                }
            )
        }
        labels = {"content": "새댓글"}
