from rest_framework import serializers
from watchlist_app.models import Review, StreamPlatform, Watchlist

# Example using serializers.ModelSerializer


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ["watchlist"]

    def get_watchlist_name(self, object):
        return object.watchlist.title


class WatchlistSerializer(serializers.ModelSerializer):

    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Watchlist
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    # Below is the nested serializer field where in we have to use the field name as related name which given in mode
    watchlist = WatchlistSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"
