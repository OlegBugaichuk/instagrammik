from django import forms
from .models import Post, Comment, Profile


class PostForm(forms.ModelForm):

    class Meta:
        # Указываем модель 
        model = Post

        # Указываем нужные поля
        fields = ['description', 'image']

        # Переопределяем labels
        labels = {
            'description': 'Описание поста',
            'image': 'Выберите картинку'
        }

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание поста'}),
            # 'image': forms.ClearableFileInput(attrs={'type': 'file', 'class': 'form-control-file'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст комментрия'})
        }


class UpdateProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        label="Дата рождения", input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format=('%d-%m-%Y'), attrs={
            'class': 'form-control',
            'placeholder': 'Дата рождения в формате  dd-mm-yyyy'
        })
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'about']
        labels = {
            'about': 'Обо мне',
            'avatar': "Аватар"
        }
        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Обо мне'})
        }