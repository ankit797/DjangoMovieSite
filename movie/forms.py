
from django import forms
from django.contrib.auth.models import User
from movie.models import userprofile
from .models import MovieList,song, video

class MovieCreate(forms.ModelForm):

	class Meta:
	    model = MovieList
	    fields = ['movie_name','movie_year' , 'movie_logo', 'is_favorite']

class SongCreate(forms.ModelForm):

    class Meta:
        model = song
        fields = ['song_name','song_type','song_audio','is_favorite']
    

class AddVideo(forms.ModelForm):

    class Meta:
        model = video
        fields = ['video_name', 'genre', 'release_year', 'video_logo', 'video_song']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required= True)

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required= True)

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name']


class DateInput(forms.DateInput):
    input_type = 'date'

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget =DateInput())

    class Meta:
        model = userprofile
        fields = ['phone_number','date_of_birth' ,'gender' , 'profile_photo', 'bio']
