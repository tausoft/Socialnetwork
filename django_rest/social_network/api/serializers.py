from rest_framework import serializers
from social_network.models import Messages


class MessagesSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Messages
        exclude = ["updated_at"]
    
    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_likes_count(self, instance):
        return instance.liked.all().count()
