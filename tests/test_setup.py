from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase

class TestSetUp(APITestCase):

    def setUp(self):
        from apps.users.models import User

        faker = Faker()

        self.login_url = '/login/'
        self.user = User.objects.create_superuser(
            name='Developer',
            last_name='Developer',
            username=faker.name(),
            password='developer',
            email=faker.email()
        )
        
        response = self.client.post( # cliet es una variable que viene de APITtestCase, y simula un cliente, para hacer las pruebas
            self.login_url,
            {
                'username': self.user.username,
                'password': 'developer'
            },
            format='json'
        )
    
        self.assertEqual(response.status_code, status.HTTP_200_OK) # verifica los dos valores separados por ,
        #import pdb; pdb.set_trace() #detiene la ejecucion, y podes llamar a cualquier variable que tengas declarada hata ese momento, por ejemplo poner response.data
        # asi sabemos que hasta aca esta todo correcto
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        return super().setUp()   
    
    # siempre ejecuta funciones que empiezan con test
    '''
    def test_algo(self):
        print(self.token)
    '''
# se ejecuta desde la terminal llamando a: python manage.py test
# la idea es que este setup se llama cuando llames a cualquier prueba unitaria para tener el tocken del usuario
