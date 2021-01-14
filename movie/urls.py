from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.home, name='home_page'),
    path('movie_list/', views.index, name = 'index'),
    path('movie_list/<int:pk>/', views.detail, name = 'detail'),
    path('movie_add/', views.create_movie, name = 'movie-add'),
    path('movie_list/<int:pk>/update/', views.MovieUpdate.as_view(), name='movie-update'),
    path('movie_list/<int:movie_id>/delete/', views.delete_movie, name='movie-delete'),

    path('movie_list/delete_all_movie/', views.delete_all_movie, name='movie-all-delete'),

    path('search/', views.search, name='search'),

    #-------------song section-----------------------
    path('song_list/<str:filter_by>/', views.songs, name='song-list'),
    path('<int:pk>/song_add/', views.create_song, name='song-add'),
    path('<int:movie_id>/song_update/<int:pk>/', views.update_song.as_view(), name='song-update'),
    path('<int:movie_id>/song_delete/<int:song_id>/', views.delete_song, name='song-delete'),

    path('<int:movie_id>/all_song_delete/', views.delete_all_song, name='song-all-delete'),

    #-----------------------favorite------------------
    path('<int:song_id>/favorite/', views.favorite, name='favorite'),
    path('<int:movie_id>/favorite_movie/', views.favorite_movie, name='favorite_movie'),

    #--------------video section----------------------
    path('video/', views.Video, name='video'),
    path('video/add_video/', views.create_video, name='add_video'),
    path('video/<int:pk>/', views.Videopage, name = 'videopage'),
    path('video/<int:pk>/update/', views.UpdateVideo.as_view(), name = 'update_video'),
    path('video/<int:video_id>/delete', views.delete_video, name='delete_video'),

    path('video/delete_all_video/', views.delete_all_video, name='video-all-delete'),

    #----------------User signup and login------------
    path('signup/', views.Signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('user/update/', views.edit_names, name = 'update_user'),

    # Forget Password
    # Change Password
    # if you singhed in then you can use change password but if you are not sign in then use password-reset option
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='movie/commons/change-password.html',
            success_url = '/movie/change-password-complete/'
        ),
        name='change_password'
    ),
    path('change-password-complete/',views.PasswordChangeComplete, name='change_password_complete'),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='movie/commons/password-reset/password_reset.html',
             subject_template_name='movie/commons/password-reset/password_reset_subject.txt',
             email_template_name='movie/commons/password-reset/password_reset_email.html',
             success_url='/movie/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='movie/commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='movie/commons/password-reset/password_reset_confirm.html',
             success_url='/movie/password-reset-complete/'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='movie/commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]
