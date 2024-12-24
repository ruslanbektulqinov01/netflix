from datetime import date
from rest_framework import serializers

from netflix_app.models import Movie, Actor, Comment


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ActorSerializer(serializers.Serializer):
    name = serializers.CharField()
    gender = serializers.CharField()
    birthdate = serializers.DateField()
    movies = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(),many=True, required=False)

    def validate_birthdate(self, value):
        min_date = date(1950, 1, 1)
        if value <= min_date:
            raise serializers.ValidationError("Birthdate must be after 01.01.1950.")
        return value

    def create(self, validated_data):
        movies = validated_data.pop('movies', [])
        actor = Actor.objects.create(**validated_data)
        actor.movies.set(movies)
        return actor


    def update(self, instance, validated_data):
        movies = validated_data.pop('movies', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if movies is not None:
            instance.movies.set(movies)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie','text', 'created_at')
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
