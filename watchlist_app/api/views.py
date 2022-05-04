import re
from django.shortcuts import get_object_or_404
from watchlist_app.models import Review, StreamPlatform, Watchlist
from watchlist_app.api.serializers import (
    ReviewSerializer,
    StreamPlatformSerializer,
    WatchlistSerializer,
)

# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle


# Generics
# Updated code

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ReviewCreateThrottle]


    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        watchlist = Watchlist.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user
        )

        if review_queryset.exists():
            raise ValidationError("You have already posted review for this movie.")
        # To calculate avg_rating
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data["rating"]
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating + serializer.validated_data["rating"]
            ) / 2

        # To calculate number of rating
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)



class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]


    # Overriding queryset
    def get_queryset(self):
        pk = self.kwargs["pk"]
        query = Review.objects.filter(watchlist=pk)
        return query

    


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Customer permissions
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


class WatchlistListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movie = Watchlist.objects.all()
        serializer = WatchlistSerializer(
            movie,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchlistDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response(
                {"error": "Watchlist not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = WatchlistSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            movie = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response(
                {"error": "Watchlist not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = WatchlistSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):

        try:
            movie = Watchlist.objects.get(pk=pk)
            movie.delete()
            return Response(
                {"message": "Movie deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except Watchlist.DoesNotExist:
            return Response(
                {"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND
            )


# ModelViewSet for SteamPlatform ==============================


class SteamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer



class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(
            platform, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response(
                {"message": "Platform deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error": "Platform not found"}, status=status.HTTP_404_NOT_FOUND
            )




