from rest_framework import serializers
from watchlist_app.models import Review, StreamPlatform, Watchlist
# Example using serializers.ModelSerializer

class ReviewSerializer(serializers.ModelSerializer):
    # watchlist = serializers.CharField(source = 'watchlist.title')
    # watchlist_name = serializers.SerializerMethodField()
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ["watchlist"]
        # fields = ["rating","description","watchlist"]
        # fields = ["rating","description","watchlist_name"]
        
    def get_watchlist_name(self, object):
        return object.watchlist.title

class WatchlistSerializer(serializers.ModelSerializer):
    # Costomer serializer field 
    # len_name = serializers.SerializerMethodField()
    review = ReviewSerializer(many = True, read_only =True)
    
    class Meta:
        model = Watchlist
        fields = "__all__"
        # fields = ['id', 'name', 'description'] 
        # exclude =['name']


class StreamPlatformSerializer(serializers.ModelSerializer):
    # Below is the nested serializer field where in we have to use the field name as related name which given in mode
    watchlist = WatchlistSerializer(many = True, read_only =True)
    # watchlist = serializers.StringRelatedField(many = True)
    # watchlist = serializers.PrimaryKeyRelatedField(many = True, read_only =True)
    # watchlist = serializers.HyperlinkedRelatedField(many = True, read_only =True, view_name='movie-details')
    
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"










    
    # # Costomer serializer field method
    # def get_len_name(self, object):
    #     length = len(object.name)
    #     return length
    
    
    # # Field level Validations
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError('Name is too short!')
    #     return value
    
    
    # # Object level Validations
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and description should be different")
    #     else:
    #         return data










# Example using serializers.Serializers

# Validators
# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")
    

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
        
        
    
#     # Field level Validations
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError('Name is too short!')
#     #     return value
    
    
#     # Object level Validations
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and description should be different")
#         else:
#             return data