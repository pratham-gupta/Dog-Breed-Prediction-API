from rest_framework import serializers
from api.models import UploadImage
from drf_extra_fields.fields import Base64ImageField


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ['image']

# class ImageUploadSerializer(serializers.Serializer):
#     image = serializers.ImageField(max_length=100,allow_empty_file=False,use_url=True)

class Base64ImageSerializer(serializers.Serializer):
    base64string = serializers.CharField(max_length=100000,allow_blank=False)


    # image = Base64ImageField()

    # class Meta:
    #     model = UploadImage
    #     fields = ['image']

    # def create(self,validated_data):
    #     image = validated_data.pop('image')
    #     return UploadImage.objects.create(image=image)
