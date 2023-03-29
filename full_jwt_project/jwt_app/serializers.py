from rest_framework import serializers
from jwt_app.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},
                                    write_only=True)
    class Meta:
        model=User
        fields=["email", "name", "password", "password2", "tc"]
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def validate(self, attrs):
        password= attrs.get("password")
        password2= attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        model=User
        fields=["email","password"]
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["id","email","name"]
        
class ChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, style={"input_type":"password"},write_only=True)
    password2=serializers.CharField(max_length=255, style={"input_type":"password"},write_only=True)
    
    class Meta:
        fields=["password","password2"]
    
    def validate(self, attrs):
        password= attrs.get("password")
        password2= attrs.get("password2")
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        user.set_password(password)
        user.save()
        return attrs