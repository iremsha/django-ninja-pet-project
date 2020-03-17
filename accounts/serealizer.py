from rest_framework import serializers


class ResultSerealizer(serializers.Serializer):
    uuid = serializers.CharField()
    name = serializers.CharField()
    balance = serializers.IntegerField()
    hold = serializers.IntegerField()
    status = serializers.BooleanField()

