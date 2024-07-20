from rest_framework import serializers

from TURO.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ["user", "vehicle"]
