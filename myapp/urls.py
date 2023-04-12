from django.urls import path, include
from .views import CustomRegistrationView, CustomLoginView, CustomLogoutView, ShowProfilePageView, CreateProfilePageView, EditProfilePageView
from .api_views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', CustomRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    path('', views.index, name='index'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('arcticles/', views.HomeListView.as_view(), name = 'arcticles'),
    path('detail/<int:pk>', views.HomeDetailView.as_view(), name = 'detail'),
    path('edit-page/', views.ArcticleCreateView.as_view(), name='edit'),
    path('create-page/', views.ArcticleCreatePage.as_view(), name='create'),
    path('update-page/<int:pk>', views.ArcticleUpdateView.as_view(), name='update'),
    path('delete-page/<int:pk>', views.ArcticleDeleteView.as_view(), name='delete'),
    path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),    
    path('create_profile_page/',CreateProfilePageView.as_view(), name='create_user_profile'),
    path('edit_profile_page/<int:pk>/',EditProfilePageView.as_view(), name='edit_user_profile'),
    # path('like_arcticle/', views.like_arcticle, name='like_arcticle'),
    path('like/', views.like_arcticle, name='like_arcticle'),
    path('unlike/', views.unlike_arcticle, name='unlike_arcticle'),  

#api urls
    path('api-arcticles/', ArcticleList.as_view(), name='api-arcticles'),
    path('api/register/', RegisterAPI.as_view(), name='register_api'),
    # path('api/login/', LoginAPI.as_view(), name='login_api'),
    path('api-detail/<int:pk>/', ArcticleDetail.as_view(), name='api-detail'),
    path('api-comments/',CommentsList.as_view(), name = 'api-comments'),
    path('article_comments/<int:pk>/',ArcticleCommentsList.as_view(), name = 'api_comments_article'),
    path('create_comment/', CommentsCreateView.as_view(), name='create_comment'),
    path('api-create/',ArcticleCreateAPIView.as_view(), name = 'api-create'),
    
    path('api-like/', LikeListCreateAPIView.as_view(), name='like_api'),
    path('api-setLike/', create_like, name='set_like_api'),
    path('delete_like/<int:pk>/', DeleteLike.as_view(), name='delete-like'),

    path('profiles/create/', ProfileCreateAPIView.as_view(), name='create-profile'),
    path('profiles/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='show-profile'),
    path('profiles/edit/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile-detail'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)