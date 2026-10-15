from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserRegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeat_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """Prüft, ob Passwort und Passwortbestätigung identisch sind."""
        if data["password"] != data["repeat_password"]:
            raise serializers.ValidationError("Invalid request data.")
        return data

    def get_response(self, obj):
        """Erzeugt bei Bedarf ein Auth-Token und formatiert die Registrierungsantwort."""
        token, _ = Token.objects.get_or_create(user=obj)
        return {
            "token": token.key,
            "fullname": obj.fullname,
            "email": obj.email,
            "user_id": obj.id
        }
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def get_response(self, obj):
        """Erzeugt bei Bedarf ein Auth-Token und formatiert die Login-Antwort."""
        token, _ = Token.objects.get_or_create(user=obj)
        return {
            "token": token.key,
            "fullname": obj.fullname,
            "email": obj.email,
            "user_id": obj.id
        }