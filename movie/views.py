from django.views import generic
from .models import MovieList,song, video , userprofile
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm,UserUpdateForm, UserProfileForm, MovieCreate, AddVideo , SongCreate
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from datetime import date

from django.contrib import messages


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']

@login_required
def home(request):
    movies = MovieList.objects.filter(user=request.user)
    videos = video.objects.filter(user=request.user)
    count= movies.count()+1
    count_videos= videos.count()+1
    
    context= {'movies': movies, 'videos':videos,'range': range(count), 'range1': range(count_videos)}
    return render(request,'movie/home.html',context);


@login_required
def search(request):
    movies = MovieList.objects.filter(user=request.user)

    song_ids = []
    for movie in movies:
        for songs in movie.song_set.all():
           song_ids.append(songs.pk)
    users_songs = song.objects.filter(pk__in=song_ids)

    videos = video.objects.filter(user=request.user)

    query = request.GET.get("q")

    if query:
        movies = movies.filter(
            Q(movie_name__icontains=query) |
            Q(movie_year__icontains=query)
        ).distinct()

        song_results = users_songs.filter(
            Q(song_name__icontains=query)
        ).distinct()

        videos = videos.filter(
            Q(video_name__icontains=query)
        ).distinct()

        if (movies or song_results or videos):
            return render(request, 'movie/search.html', {
                'movies': movies,
                'songs': song_results,
                'videos':videos,
                'found_query':query,
            })

        else:
            return render(request, 'movie/search.html',{'query':query})


    else:
        result = "You have not search any thing."
        return render(request, 'movie/search.html',{'result':result})


@login_required
def index(request):
    movies = MovieList.objects.filter(user=request.user)

    return render(request, 'movie/index.html', {'movies': movies})


@login_required
def detail(request, pk):
    user = request.user
    movie = get_object_or_404(MovieList, pk=pk)
    return render(request, 'movie/detail.html', {'movie': movie, 'user': user})

#------------------------Movie Section-----------------------------------

@login_required
def create_movie(request):
    form = MovieCreate(request.POST or None, request.FILES or None)
    if form.is_valid():
        movie = form.save(commit=False)
        movie.user = request.user
        movie.movie_logo = request.FILES['movie_logo']

        movie.save()
        return render(request, 'movie/detail.html', {'movie': movie})

    context = {
        "form": form,
    }
    return render(request, 'movie/create_movie.html', context)


class MovieUpdate(UpdateView):
    model = MovieList
    fields = ['movie_name', 'movie_year', 'movie_logo','is_favorite']
    


def delete_movie(request, movie_id):
    movies = MovieList.objects.filter(user=request.user)
    movie = get_object_or_404(MovieList, pk=movie_id)
    movie.delete()
    return render(request, 'movie/index.html', {'movies': movies})


def delete_all_movie(request):
    Error =""
    username = request.user.username

    if request.method == "POST":
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:

                movies = MovieList.objects.filter(user=request.user)
                movies.delete()
            else:
                Error ="User is Not Active"
        else:
            Error ="Can't Delete Movies , Wrong Password!"

    movies = MovieList.objects.filter(user=request.user)
    return render(request, 'movie/index.html',{'movies':movies,'Error':Error})



#-------------------------------------song section-------------------------------------
@login_required
def songs(request, filter_by):
    try:
        song_ids = []
        for movie in MovieList.objects.filter(user=request.user):
            for songs in movie.song_set.all():
                song_ids.append(songs.pk)
        users_songs = song.objects.filter(pk__in=song_ids)
        if filter_by == 'favorites':
            users_songs = users_songs.filter(is_favorite=True)
    except MovieList.DoesNotExist:
        users_songs = []
    return render(request, 'movie/song_list.html', {
        'all_songs': users_songs,
        'filter_by': filter_by,
    })


def create_song(request, pk):
    form = SongCreate(request.POST or None, request.FILES or None)
    movie = get_object_or_404(MovieList, pk=pk)
    if form.is_valid():
        albums_songs = movie.song_set.all()
        for s in albums_songs:
            if s.song_name == form.cleaned_data.get("song_name"):
                context = {
                    'movie': movie,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'movie/create_song.html', context)
        song = form.save(commit=False)
        song.movie = movie
        song.song_audio = request.FILES['song_audio']


        file_type = song.song_audio.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
            'movie':movie,
            'form':form,
            'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'movie/create_song.html', context)

        song.save()
        return render(request, 'movie/detail.html', {'movie': movie})
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movie/create_song.html', context)


class update_song(UpdateView):
    model = song
    fields = ['movie','song_name','song_type','song_audio','is_favorite']


def delete_song(request, movie_id, song_id):
    movie = get_object_or_404(MovieList, pk=movie_id)
    songs = song.objects.get(pk=song_id)
    songs.delete()
    return render(request, 'movie/detail.html', {'movie': movie})



def delete_all_song(request, movie_id):  # delete all songs from an album
    Error =""
    username = request.user.username
    movies = MovieList.objects.filter(user=request.user)
    movie = movies.filter(pk=movie_id)
    song_ids = []
    for movie in movies.filter(pk=movie_id):
        for songs in movie.song_set.all():
            song_ids.append(songs.pk)
    users_songs = song.objects.filter(pk__in=song_ids)

    if request.method == "POST":
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:

                users_songs.delete()
            else:
                Error ="User is Not Active"
        else:
            Error ="Can't Delete Songs , Wrong Password!"

    return render(request, 'movie/detail.html',{'movie':movie,'Error':Error})

#--------------------------------favorite--------------------------------------
def favorite(request, song_id):
    songs = get_object_or_404(song, pk=song_id)
    try:
        if songs.is_favorite:
            songs.is_favorite = False
        else:
            songs.is_favorite = True
        songs.save()
    except (KeyError, song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_movie(request, movie_id):
    movies = get_object_or_404(MovieList, pk=movie_id)
    try:
        if movies.is_favorite:
            movies.is_favorite = False
        else:
            movies.is_favorite = True
        movies.save()
    except (KeyError, movie.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

#---------------------------------video section-------------------------------------
@login_required
def Video(request):
    videos = video.objects.filter(user=request.user)
    return render(request, 'movie/video.html', {'all_videos': videos})

@login_required
def Videopage(request, pk):
    user = request.user
    videos = get_object_or_404(video, pk=pk)
    return render(request, 'movie/videopage.html', {'video': videos, 'user': user})

@login_required
def create_video(request):
    form = AddVideo(request.POST or None, request.FILES or None)
    if form.is_valid():
        video = form.save(commit=False)
        video.user = request.user
        video.video_logo = request.FILES['video_logo']
        video.video_song = request.FILES['video_song']

        video.save()
        return render(request, 'movie/videopage.html', {'video': video})

    context = {
        "form": form,
    }
    return render(request, 'movie/create_video.html', context)

class UpdateVideo(UpdateView):
    model = video
    fields = ['video_name', 'genre', 'release_year', 'video_logo', 'video_song']
    


def delete_video(request, video_id):
    videos = video.objects.filter(user=request.user)
    video_song = get_object_or_404(video, pk=video_id)
    video_song.delete()
    return render(request, 'movie/video.html', {'all_videos': videos})


def delete_all_video(request):
    Error =""
    username = request.user.username

    if request.method == "POST":
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:

                videos = video.objects.filter(user=request.user)
                videos.delete()
            else:
                Error ="User is Not Active"
        else:
            Error ="Can't Delete Videos , Wrong Password!"

    videos = video.objects.filter(user=request.user)
    return render(request, 'movie/video.html',{'all_videos':videos,'Error':Error})



#------------------user register and login----------------------------------------------


def Signup(request):
    form = UserForm(request.POST or None)
    profile_form = UserProfileForm(request.POST, request.FILES)
    
    if form.is_valid() and profile_form.is_valid():
        user = form.save(commit=False)
        profile = profile_form.save(commit= False)
        profile.user = user

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        profile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                movies = MovieList.objects.filter(user=request.user)

                messages.info(request, 'Your account has been created successfully!')

                return render(request, 'movie/home.html', {'movies': movies})
    context = {
        "form": form,
        "profile_form":profile_form,
    }
    return render(request, 'movie/signup.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                movies = MovieList.objects.filter(user=request.user)
                return render(request, 'movie/home.html', {'movies': movies})
            else:
                return render(request, 'movie/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'movie/login.html', {'error_message': 'Invalid login'})
    return render(request, 'movie/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'movie/login.html' , context)





@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    dob = user.userprofile.date_of_birth
    today = date.today()

    if ((today.month == dob.month) and (today.day == dob.day)):
        birthday = 'Wissing You a Very Very Happy Birthday.'
    else:
        birthday = ''

    return render(request, 'movie/profile.html', {'user': user,'birthday':birthday ,'today':today})


@login_required
def edit_names(request):
    Error =""
    if request.method == "POST":
        # line 324,325,326,327,328 for checking your password is write or wrong.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:

                form = UserUpdateForm(data=request.POST, instance=request.user)
                profile_form = UserProfileForm(request.POST, instance= request.user.userprofile)
                if form.is_valid() and profile_form.is_valid():
                    user = form.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    if 'profile_photo' in request.FILES:
                        profile.profile_photo = request.FILES['profile_photo']
                    profile.save()
                    url = reverse('movie:home_page')

                    return HttpResponseRedirect(url)
                else:
                    error_message =""
                    print(form.errors, profile_form.errors)
            else:
                Error ="User is Not Active"
        else:
            Error = "Wrong Password! For Update Your information you have to enter right password."

    form = UserUpdateForm(instance=request.user)
    profile_form = UserProfileForm( instance= request.user.userprofile)

    return render(request, "movie/update_user.html",{"form":form, "profile_form":profile_form,"Error":Error})

def PasswordChangeComplete(request):
    return render(request, 'movie/commons/change_password_complete.html', {})
