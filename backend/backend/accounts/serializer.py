from rest_framework import serializers
from django.contrib.auth.models import User
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        error_messages={
            'blank': 'La contraseña es obligatoria',
            'required': 'La contraseña es obligatoria'
        }
    )
    
    password2 = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        error_messages={
            'blank': 'Debes confirmar la contraseña',
            'required': 'Debes confirmar la contraseña'
        }
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'username': {
                'error_messages': {
                    'blank': 'El nombre de usuario es obligatorio',
                    'required': 'El nombre de usuario es obligatorio',
                    'max_length': 'El nombre de usuario es demasiado largo'
                },
                'validators': []  # ← Esto es importante: remueve validadores automáticos
            },
            'email': {
                'error_messages': {
                    'blank': 'El email es obligatorio',
                    'required': 'El email es obligatorio',
                    'invalid': 'Ingresa un email válido'
                },
                'validators': []  # ← Remueve validadores automáticos para email
            },
            'first_name': {
                'error_messages': {
                    'blank': 'El nombre es obligatorio',
                    'required': 'El nombre es obligatorio'
                }
            },
            'last_name': {
                'error_messages': {
                    'blank': 'El apellido es obligatorio',
                    'required': 'El apellido es obligatorio'
                }
            }
        }
        
    def validate(self, data):
        # Validación de username único
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({
                'username': 'Este nombre de usuario ya está en uso'
            })
            
        # Validación de contraseñas
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password2': 'Las contraseñas no coinciden'
            })
        
        # Validación de email único
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': 'Este email ya está registrado'
            })
        
        # Validación de fortaleza de contraseña
        if len(data['password']) < 8:
            raise serializers.ValidationError({
                'password': 'La contraseña debe tener al menos 8 caracteres'
            })
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    