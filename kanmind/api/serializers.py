from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeat_password = serializers.CharField(write_only=True, required=False)

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def get_response(self, obj):
        return {
            "token": "dummy_token",  # Replace with actual
            "fullname": obj.fullname,
            "email": obj.email,
            "user_id": obj.id
        }
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def get_response(self, obj):
        return {
            "token": "dummy_token",  # Replace with actual
            "fullname": obj.fullname,
            "email": obj.email,
            "user_id": obj.id
        }