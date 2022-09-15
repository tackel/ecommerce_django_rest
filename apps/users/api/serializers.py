from rest_framework import serializers
#from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User
'''
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','name','last_name')
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    '''
    def to_representation(self, instance):
        return { # de eesta manera podes filtral lo que se muestra en el get y cambiar los nombres a los campos sin modificar modelo ni bd ni nada
            'id': instance['id'], # uso corchetes por que es un diccionario, si en la vista solo uso .objects.all() debo usar intance.id
            'nombre_usuario': instance['username'],
            'correo': instance['email'],
            'clave': instance['password']
        }
    '''

    def create(self,validated_data):
        user = User(**validated_data)
        # Encriptar la contraseña
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user



'''
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')





class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Debe ingresar ambas contraseñas iguales'}
            )
        return data
'''
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password']
        }



# EJEMPLO DE COMO VALIDA UN SERIALIZADOR
#busca primero si hay una funcion que empiece con validate_ y el nombre del campo a validar. y luego pasa al siguiente campo
# al final hace la validacion general
# si uso el serializer basado en un MODELO, django esto lo ahce automaticamente
'''
class TestUserSerializer(serializer.Serializer):
    name = serializers.CharField(max_length = 200)
    email = serializers.EmailField()

    def validate_name(self, value):
        if 'pepito' in value:
            print('no puede existir un usuarioc on este nombre')
            raise serializers.ValidationError('Error, no puedo exitir este usuario')
        return value
    #puedo pasar el context y validar un dato de name y el email
    def validate_email(self, value):
        if value == '':
            raise serializers.ValidationError('tiene que indicar un correo')
        # para usar el context tenes que enviarlo por parametro en la instancia del serializador en la vista.
        if self.validate_name(self.context['name']) in value: # de esta forma el erro le figurara al campo email especifico
            raise serializers.ValidationError('El email no puede contener el nombre')
        print(valur)
        return value

    def validate(self, data):
        if data['name'] in data['email']:
            raise serializers.ValidationError('el email no puede contener el nombre')
        print('validacion general')
        return data

    def create(self, validated_data): # entra a esta funcion cuando pones el .save( )
        return User.objects.create(**validated_data) #en este caso seria User, pero en reliada busca el model que se paso en la clase meta model.object.create

    # al llamar al metodo PUT para actualizar el .save no llama al metodo create sino al update
    def update(self, intance, validated_data):
        instance.name = validated_data.get('name',instace.name) # esto lo hace por cada campo que hay en el objeto
        instance.save()
        return intance

'''