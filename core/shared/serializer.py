from core.models import Employee, Vaccination
from rest_framework.serializers import ModelSerializer,CharField,Serializer,SerializerMethodField
from rest_auth.serializers import PasswordResetSerializer

class VaccinationSerializer(ModelSerializer):
    type =  CharField(source='type.type')
    class Meta:
        model = Vaccination
        fields = ['id','type','number_doses','date']

class EmployeeSerializer(ModelSerializer):
    vaccine = SerializerMethodField()
    class Meta:
        model = Employee
        fields = '__all__'
    def get_vaccine(self,obj):
        data =  Vaccination.objects.filter(employee=obj)
        res = VaccinationSerializer(data,many=True)
        return res.data


class AuthTokenSerializer(Serializer):
    grand_type = CharField()
    client_secret =  CharField()
    username =  CharField()
    password =  CharField()
    client_id =  CharField()



        
class ResponseSerializer(Serializer):
    message = CharField()
    type = CharField()



class CustomPasswordResetSerializer(PasswordResetSerializer):
    url = CharField()
    
    def get_email_options(self):

        data = {
            'email_template_name': 'password_reset.html',
            'subject_template_name': 'password_reset_subject.txt',
            'extra_email_context':{
                'fronted':  self.validated_data['url']
            }
        }
        return data