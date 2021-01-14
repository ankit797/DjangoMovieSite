from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class MovieList(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length= 200)
    movie_year = models.CharField(max_length= 5)
    movie_logo = models.ImageField(upload_to = 'movie_logo/')
    is_favorite = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('movie:detail', kwargs = {'pk': self.pk})

    def __str__(self):
        return self.movie_name + ' - ' + self.movie_year


class song(models.Model):
    movie = models.ForeignKey(MovieList,  on_delete= models.CASCADE)
    song_name = models.CharField(max_length = 200)
    song_type = models.CharField(max_length = 20)
    song_audio = models.FileField(upload_to = 'song/')
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('movie:detail', kwargs = {'pk': self.movie.id})

    def __str__(self):
        return self.song_name


class video(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    video_name = models.CharField(max_length= 300)
    genre = models.CharField(max_length= 40)
    release_year = models.CharField(max_length= 4)
    video_logo = models.ImageField(upload_to = 'video_logo/')
    video_song = models.FileField(upload_to = 'video_song/')

    def get_absolute_url(self):
        return reverse('movie:videopage', kwargs = {'pk': self.pk})

    def __str__(self):
        return self.video_name + '-' + self.release_year


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/user_{0}/{1}'.format(instance.user.id, filename)


class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length= 10)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to=user_directory_path, blank=True)
    date_of_birth = models.DateField(max_length=10, blank=True,null=True)
    GENDER_CHOICES = (
	(None,'Select gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    def get_absolute_url(self):
        return reverse('movie:index')

    def __str__(self):
        return self.user.username




