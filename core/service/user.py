from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from core.shared.utils import Util


def create_user(data,current_site):
    password = User.objects.make_random_password()
    email_body = 'Se ha creado su cuenta en el sitio {} \n\n' \
                    'Su usuario es el siguiente: {} \n\n' \
                    'Contraseña Temporal: {}'\
                    '¡Gracias por usar el sitio! \n\n' \
                    'El equipo de {}'.format(str(current_site), data.get("username"),password,str(current_site))


    password = make_password(password, salt=None, hasher='default')
    user =  User.objects.create(username=data.get('username'),
                                 email=data.get('email'),
                                 password=password,
                                 first_name=data.get('first_name'),
                                 last_name=data.get('last_name')
                                 )
    
    if user:
        Util.send_email({'email_subject':'Usuario Creado','email_body':email_body,'to_email':data.get('email')})
    return user


def delete_user_by_id(id):
    User.objects.filter(pk=id).delete()

