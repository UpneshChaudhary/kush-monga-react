import re
from rest_framework import serializers
from listings.models import Listing, HomeOpen, ComingSoon
from realtors.models import Realtor
from .models import SoldProperty, Certificate, Award, About, Blog, TextReview, FeedbackCard
from listings.models import HomeOpen, Listing
from contacts.models import MarketAppraisal, Registered_User
from .models import Award, Certificate


class ListingSerializer(serializers.ModelSerializer):
    photo_main = serializers.SerializerMethodField()

    def get_photo_main(self, obj):
        request = self.context.get('request')
        if obj.photo_main:
            return request.build_absolute_uri(obj.photo_main.url)
        return None

    class Meta:
        model = Listing
        fields = '__all__'

# Sold Property Serializer
class SoldPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldProperty
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None




# Certificate Serializer
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

# Award Serializer
class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'

# About Serializer
class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'

# Feedback Card Serializer
class FeedbackCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackCard
        fields = '__all__'



# Text Review Serializer
class TextReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextReview
        fields = '__all__'

# Home Open Serializer
class HomeOpenSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeOpen
        fields = '__all__'

# Coming Soon Serializer
class ComingSoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComingSoon
        fields = '__all__'

# Realtor Serializer
class RealtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realtor
        fields = '__all__'




class GroupedHomeOpenSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = HomeOpen
        fields = ['listing', 'image', 'title', 'address', 'events']

    def get_events(self, obj):
        home_opens = HomeOpen.objects.filter(listing=obj.listing)
        return [
            {
                "date": home_open.date,
                "day": home_open.day,
                "start_time": home_open.start_time,
                "end_time": home_open.end_time,
            }
            for home_open in home_opens
        ]




class VideoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    videoId = serializers.SerializerMethodField()
    title = serializers.CharField()

    class Meta:
        model = Listing  # Use Listing instead of Video
        fields = ['id', 'video', 'title', 'videoId']  # Ensure 'video' exists in Listing

    def get_videoId(self, obj):
        """
        Extracts the YouTube video ID from various YouTube URL formats.
        """
        if not obj.video:
            return None

        # Regular expression to extract YouTube video ID
        youtube_regex = (
            r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        )

        match = re.search(youtube_regex, obj.video)
        return match.group(1) if match else None




class MarketAppraisalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketAppraisal
        fields = '__all__'



class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registered_User
        fields = '__all__'



class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'title', 'image', 'created_at']

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'title', 'description', 'image']
