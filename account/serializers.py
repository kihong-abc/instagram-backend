from django.contrib.auth import authenticate
from rest_framework_jwt.compat import PasswordField
from rest_framework_jwt.settings import api_settings
from .models import Profile
from rest_framework import serializers


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email']


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class SignupSerializerWithToken(serializers.ModelSerializer):
    """
    username 과 password 를 입력하면 회원가입을 하고, token 을 리턴함
    """
    token = serializers.SerializerMethodField()
    password = PasswordField(write_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ['token', 'username', 'password']

    def get_token(self, obj):
        # token 리턴
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializerWithToken(serializers.ModelSerializer):
    """
    username, password 의 validation 을 확인한 뒤 토큰 리턴
    토큰 이외의 값을 리턴하고자 할 땐 jwt_payload_handler setting 을 수정해야 함.
    """
    username = serializers.CharField()
    password = PasswordField(write_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'password']

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                # if not user.is_active:
                #     msg = 'User account is disabled.'
                #     raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            # else:
            #     msg = 'Unable to log in with provided credentials.'
            #     raise serializers.ValidationError(msg)
        # else:
        #     msg = 'Must include "{username_field}" and "password".'
        #     msg = msg.format(username_field=self.username_field)
        #     raise serializers.ValidationError(msg)

    @property
    def object(self):
        return self.validated_data
