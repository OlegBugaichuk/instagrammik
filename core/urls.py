from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, LogoutView
)
from django.contrib.staticfiles.urls import static
from django.conf import settings
from .views import (
    IndexView, FeedView, PostView, CreatePostView, 
    DeletePostView, EditPostView, like_post, AddRemoveFriend, EditProfileView, 
    ProfileView
)
from .views_auth import LoginView

app_name='core'

urlpatterns = [
    url(r'^posts/$', IndexView.as_view(), name='index'),
    path('posts/feed/', FeedView.as_view(), name='post-feed'),
    path('posts/create/', CreatePostView.as_view(), name='post-create'),
    path('posts/<int:post_id>/', PostView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/edit/', EditPostView.as_view(), name='post-edit'),
    path('posts/<int:post_id>/delete/', DeletePostView.as_view(), name='post-delete'),
    path(
        'posts/<int:post_id>/delete_success/', 
        TemplateView.as_view(template_name='core/delete_success.html'), 
        name='post-delete-success'
    ),
    path('posts/<int:post_id>/like/', like_post, name='post-like'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_reset/', PasswordResetView.as_view(success_url=reverse_lazy('core:password_reset_done'),
                                                      email_template_name='my_auth/password_reset_email.html',
                                                      template_name='my_auth/password_reset.html'),
         name='password_reset'),

    path('password_reset/done', PasswordResetDoneView.as_view(template_name='my_auth/password_reset_done.html'),
         name='password_reset_done'),

    path('password_reset/<str:uidb64>/<slug:token>', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('core:password_reset_complete')), name='password_reset_confirm'),

    path('password_reset/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('<int:user_id>/profile/', ProfileView.as_view(), name='profile'),
    path('<int:user_id>/profile/add_remove_friend/', AddRemoveFriend.as_view(), name='add-remove-friend'),
    path('<int:user_id>/profile/edit/', EditProfileView.as_view(), name='edit-profile')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)