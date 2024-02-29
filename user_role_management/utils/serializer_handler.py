from rest_framework import serializers


class CustomSingleResponseSerializerBase(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)


class CustomMultiResponseSerializerBase(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()


class FilterSerializerBase(serializers.Serializer):
    limit = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)


class FilterWithSearchSerializerBase(FilterSerializerBase):
    search = serializers.CharField(max_length=100, required=False)
