import re
from django.shortcuts import get_object_or_404
from watchlist_app.models import Review, StreamPlatform, Watchlist
from watchlist_app.api.serializers import ReviewSerializer, StreamPlatformSerializer, WatchlistSerializer
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError 


# Generics

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    # Overriding queryset
    def get_queryset(self):
        pk = self.kwargs['pk']
        query = Review.objects.filter(watchlist=pk)
        return query
    
    # def watchlist_data(self,request):
    #     data = 
    
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
     
    
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        watchlist = Watchlist.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user = review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already posted review for this movie.")
        
        
        serializer.save(watchlist = watchlist, review_user = review_user)
        
    
    
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer





# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    

# class ReviewDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
    

# View for Watchlist ==============================

class WatchlistListAV(APIView):
    def get(self,request):
        movie = Watchlist.objects.all()
        serializer = WatchlistSerializer(movie, many=True, )
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    
    def post(self,request):
        serializer = WatchlistSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class WatchlistDetailsAV(APIView):
    def get(self, request, pk):
        try:
            movie = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({
                'error': 'Watchlist not found'
            }, status = status.HTTP_404_NOT_FOUND)
        serializer = WatchlistSerializer(movie)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            movie = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({
                'error': 'Watchlist not found'
            }, status = status.HTTP_404_NOT_FOUND)
        serializer = WatchlistSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)      
    
    def delete(self,request, pk):
        
        try:
            movie = Watchlist.objects.get(pk=pk)
            movie.delete() 
            return Response({
                'message': 'Movie deleted'
            }, status = status.HTTP_204_NO_CONTENT)
        except Watchlist.DoesNotExist:
            return Response({
                'error': 'Movie not found'
            }, status = status.HTTP_404_NOT_FOUND)
            
            
# ModelViewSet for SteamPlatform ==============================
            
class SteamPlatformVS(viewsets.ModelViewSet): 
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer







# ViewSet for SteamPlatform ==============================

# class SteamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)


#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


#     def delete(self, request, pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#             platform.delete()
#             return Response({
#                 'message': 'Platform deleted'
#             }, status = status.HTTP_204_NO_CONTENT)
#         except StreamPlatform.DoesNotExist:
#             return Response({
#                 'error': 'Platform not found'
#             }, status = status.HTTP_404_NOT_FOUND)


# View for SteamPlatform ==============================

class StreamPlatformAV(APIView):
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True,context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

class StreamPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response({
                'message': 'Platform deleted'
            }, status = status.HTTP_204_NO_CONTENT)
        except StreamPlatform.DoesNotExist:
            return Response({
                'error': 'Platform not found'
            }, status = status.HTTP_404_NOT_FOUND)
            


# View for Review using APIView ==============================

class _ReviewListAV(APIView):
    def get(self, request):
        review = Review.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.error, status= status.HTTP_400_BAD_REQUEST)
    
    

class _ReviewDetailsAV(APIView):
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'message': 'Review not found'})
            
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'message': 'Review not found'})
        serializer = ReviewSerializer(review, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response({'message':"Review deleted"}, status = status.HTTP_204_NO_CONTENT)
        except Review.DoesNotFound:
            return Response({'message':'Review not found'}, status = status.HTTP_404_NOT_FOUND)
        
        














# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if(request.method == 'GET'):
#         movies = Movie.objects.all()
#         # print(movies)
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     if(request.method == 'POST'):
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
          


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if(request.method == 'GET'):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({
#                 "Error":"Movie does not exist"
#             },status=status.HTTP_404_NOT_FOUND
#            )
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if(request.method == 'PUT'):
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     if(request.method == 'DELETE'):
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response({
#             'mesg':'This data is deleted'
#         }, status = status.HTTP_204_NO_CONTENT)
