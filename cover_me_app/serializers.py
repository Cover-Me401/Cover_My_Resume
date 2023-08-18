from rest_framework import serializers
from .models import Coverletter


class CoverletterSerializer(serializers.ModelSerializer):
  class Meta:
    model = Coverletter
    fields = "__all__"