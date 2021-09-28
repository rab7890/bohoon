from rest_framework import serializers

from mainapp.models import GroupEvent, Member


class GroupEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupEvent
        fields = '__all__'
        depth = 2

class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = '__all__'
        depth = 2
    