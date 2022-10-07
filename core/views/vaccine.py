from email import message
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from core.shared.permissions import UserPermission
from rest_framework.serializers import ModelSerializer,CharField,PrimaryKeyRelatedField, EmailField,\
    Serializer,DateField,BooleanField, IntegerField,SlugRelatedField
from core.models import Vaccine
from core.service.vaccine import create_vaccine, get_all_vaccine
from core.shared.serializer import ResponseSerializer
from drf_yasg.utils import swagger_auto_schema



class CreateVaccine(APIView):
    model = Vaccine
    permission_classes= [IsAuthenticated,UserPermission]
    permission_required = 'core.add_vaccine'

    class VacineCreateSerializer(Serializer):
        type = CharField()
        is_active = BooleanField()


    @swagger_auto_schema(
            tags=["Vacunas"],
            operation_summary="Crear Vacuna",
            request_body=VacineCreateSerializer(),
            responses={
                200: ResponseSerializer(),
            }
    )
    def post(self,request):
        data = self.VacineCreateSerializer(data=request.data)
        if data.is_valid():
            create_vaccine(data.data)
            res = ResponseSerializer({"message":"Vaccine Created","type":'SUCCESS'})
            return Response(res.data,status=status.HTTP_201_CREATED)
        else:
            m = ""
            for i in data._errors.keys():
                m += i + " "+data._errors[i][0]+" "
            message = ResponseSerializer({"message":m,"type":"INVALID_FORMAT"})

            return Response(message.data,status=status.HTTP_400_BAD_REQUEST)



class GetAllVaccine(APIView):
    model = Vaccine
    permission_classes = [IsAuthenticated,UserPermission]
    permission_required = 'core.view_vaccine'
    class VaccineSerializer(ModelSerializer):
        class Meta:
            model = Vaccine
            fields = '__all__'

    @swagger_auto_schema(
            tags=["Vacunas"],
            operation_summary="Listar Vacunas",
            responses={
                200: VaccineSerializer(),
            }
    )
    def get(self,request):
        data = get_all_vaccine()
        res = self.VaccineSerializer(data,many=True)
        return Response(res.data,status=status.HTTP_200_OK)
