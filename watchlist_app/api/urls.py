from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_details, movie_list
from watchlist_app.api.views import (
    ReviewDetails,
    ReviewList,
    SteamPlatformVS,
    ReviewCreate,
    UserReview,
    WatchlistListAV,
    WatchlistDetailsAV,
    WatchlistAV
)

router = DefaultRouter()
router.register("stream", SteamPlatformVS, basename="streamplatform")


urlpatterns = [
    path("list/", WatchlistListAV.as_view(), name="movie-list"),
    path("<int:pk>/", WatchlistDetailsAV.as_view(), name="movie-details"),
    path("list2/", WatchlistAV.as_view(), name="watch-list"),
    
    
    path("", include(router.urls)),
    path("<int:pk>/review-create/", ReviewCreate.as_view(), name="review-create"),
    path("<int:pk>/review/", ReviewList.as_view(), name="review-list"),
    path("review/<int:pk>/", ReviewDetails.as_view(), name="review-details"),
    
    # path("reviews/<str:username>/", UserReview.as_view(), name="user-review-details"),
    path("reviews/", UserReview.as_view(), name="user-review-details"),
]
