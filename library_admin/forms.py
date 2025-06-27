from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Book, UserProfile


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'book_title', 'book_author', 'category', 'book_copies',
            'publication_year', 'publication_name', 'book_isbn'
        ]
        widgets = {
            'book_title': forms.TextInput(attrs={'class': 'form-control'}),
            'book_author': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'book_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_name': forms.TextInput(attrs={'class': 'form-control'}),
            'book_isbn': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    contact = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    is_staff = forms.BooleanField(required=False, label='Admin privileges')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = self.cleaned_data['is_staff']
        if commit:
            user.save()
            # Create or update user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.user_contact = self.cleaned_data.get('contact', '')
            profile.user_address = self.cleaned_data.get('address', '')
            profile.save()
        return user


class UserEditForm(forms.ModelForm):
    contact = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Pre-populate profile fields
        if self.instance.pk:
            try:
                profile = self.instance.userprofile
                self.fields['contact'].initial = profile.user_contact
                self.fields['address'].initial = profile.user_address
            except UserProfile.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Update or create user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.user_contact = self.cleaned_data.get('contact', '')
            profile.user_address = self.cleaned_data.get('address', '')
            profile.save()
        return user