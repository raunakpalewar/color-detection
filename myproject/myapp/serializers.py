from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()





class ImageURLSerializer(serializers.Serializer):
    image_url = serializers.CharField(max_length=256)