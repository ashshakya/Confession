from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from blog.models import Post, Comment, Reply
from notifications.models import Notification

User = get_user_model()


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    user_id = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255, required=False)
    success = serializers.BooleanField(default=False)


# Custom Validator for password.
def password_validate(password):
    """
    Validate Password.
    """
    if not password:
        raise serializers.ValidationError(
            {'password': 'Password cannot be empty!'}
        )
    elif len(password) < 8:
        raise serializers.ValidationError(
            {'password': 'Password too short.'}
        )


class RegisterSerializer(serializers.ModelSerializer):

    user_check = UniqueValidator(
        queryset=User.objects.all(),
        message='username already exists'
    )
    email_check = UniqueValidator(
        queryset=User.objects.all(),
        message='Email already exists'
    )
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(
        required=True,
        max_length=100,
        validators=[email_check]
    )
    username = serializers.CharField(
        required=True,
        validators=[user_check]
    )
    password = serializers.CharField(
        min_length=8,
        validators=[password_validate]
    )
    is_editor = serializers.BooleanField(default=False)
    # is_chief = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'first_name', 'last_name', 'is_editor')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
    )
    password = serializers.CharField(
        max_length=100,
        validators=[password_validate]
    )


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class BlogCreateSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=255, trim_whitespace=True)
    text = serializers.CharField(allow_blank=False, trim_whitespace=True)
    owner_id = serializers.ModelField(
        model_field=User()._meta.get_field('id')
    )
    request_from = serializers.CharField(max_length=10, default='api')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post

    class Meta:
        model = Post
        fields = ('title', 'text', 'owner_id', 'request_from')


class CommentSerializer(serializers.ModelSerializer):

    comment = serializers.CharField(allow_blank=False, trim_whitespace=True)
    blog_id = serializers.ModelField(model_field=Post()._meta.get_field('id'))
    user_id = serializers.ModelField(model_field=User()._meta.get_field('id'))

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    class Meta:
        model = Comment
        fields = ('comment', 'blog_id', 'user_id')


class ReplySerializer(serializers.ModelSerializer):

    reply = serializers.CharField(allow_blank=False, trim_whitespace=True)
    which_comment_id = serializers.ModelField(
        model_field=Comment()._meta.get_field('id')
    )
    blog_id = serializers.ModelField(model_field=Post()._meta.get_field('id'))
    user_id = serializers.ModelField(model_field=User()._meta.get_field('id'))

    def create(self, validated_data):
        reply = Reply.objects.create(**validated_data)
        return reply

    class Meta:
        model = Reply
        fields = ('reply', 'which_comment_id', 'blog_id', 'user_id')


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
