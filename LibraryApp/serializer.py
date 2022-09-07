
from rest_framework import serializers
from .models import Books, User



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'password','is_librarian','is_member')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = ('id','name','status')


class BookLibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('id','name','status','added_by','borrowed_by')

class SearchSerializer(serializers.Serializer):
    search = serializers.CharField()