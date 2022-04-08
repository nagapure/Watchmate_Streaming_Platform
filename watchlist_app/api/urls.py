from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_details, movie_list
from watchlist_app.api.views import  (
    ReviewDetails, ReviewList, SteamPlatformVS , ReviewCreate,
    WatchlistListAV, WatchlistDetailsAV 
    # StreamPlatformAV,
    # StreamPlatformDetailAV
    )

router = DefaultRouter()
router.register('stream', SteamPlatformVS, basename = 'streamplatform')


urlpatterns = [
    path('list/', WatchlistListAV.as_view(), name='movie-list'),
    path('list/<int:pk>', WatchlistDetailsAV.as_view(), name='movie-details'),
    
    path('', include(router.urls)),
    
    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-details'),
    
    # This review urls for model Mixin
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetails.as_view(), name='review-details'),
    
    path('stream/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>', ReviewDetails.as_view(), name='review-details'),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # This review urls for APIView class
    # path('review/', ReviewListAV.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetailsAV.as_view(), name='review-details'),

    
]
