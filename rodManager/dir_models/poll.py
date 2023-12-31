from django.db import models
from rest_framework import serializers


class Poll(models.Model):
    id = models.AutoField(primary_key=True)
    end_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()


class Option(models.Model):
    id = models.AutoField(primary_key=True)
    option_id = models.IntegerField()
    label = models.CharField(max_length=200)
    poll = models.ForeignKey("Poll", on_delete=models.CASCADE, related_name="options")


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    option = models.ForeignKey("Option", on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(
        "rodManager.Account", on_delete=models.CASCADE, related_name="votes"
    )

    class Meta:
        unique_together = ("option", "user")


class OptionSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ["option_id", "label", "vote_count"]

    def get_vote_count(self, obj):
        return Vote.objects.filter(option=obj).count()


class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ["id", "title", "description", "options", "end_date", "user_vote"]

    def get_user_vote(self, obj):
        request = self.context.get("request", None)
        if request:
            vote = Vote.objects.filter(option__in=obj.options.all(), user=request.user)
            if vote:
                return vote[0].option.option_id
        return None
