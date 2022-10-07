from turtle import update
from wsgiref.validate import validator
from django.shortcuts import render
from requests import delete
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView, Response, status
from rest_framework.serializers import ModelSerializer,CharField,PrimaryKeyRelatedField, EmailField,\
    Serializer,DateField,BooleanField, IntegerField, ManyRelatedField
from rest_framework.validators import UniqueValidator
from rest_framework.generics import GenericAPIView

from core.shared.permissions import UserPermission
from core.shared.serializer import CustomPasswordResetSerializer, EmployeeSerializer, ResponseSerializer, VaccinationSerializer
from core.models import Employee, Vaccination
from core.service.employee import create_employee, delete_by_id, getAll, getByDateRange, getById, getByStatusVaccination, getByTypeVaccine, getByUserId,\
     update_employee
from core.shared.validators import NumericValidator,RequiredConditional
from core.service.vaccine import getVaccineByName
from core.service.user import create_user, delete_user_by_id
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.



class GetEmployee(APIView):
    permission_required = 'core.view_employee'
    permission_classes = [UserPermission, IsAuthenticated]
    model = Employee

    
    @swagger_auto_schema(
        tags=["Empleados"],
        operation_summary="Lista de Empleados",
        manual_parameters=[
            openapi.Parameter('state', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('type_vaccine', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('date_start', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('date_end', openapi.IN_QUERY, type=openapi.TYPE_STRING),

        ],
        responses={
            200: EmployeeSerializer(many=True),
        }
    )
    def get(self,request):
        state = request.query_params.get('state') if request.query_params.get('state')  else None
        type_vaccine = request.query_params.get('type_vaccine') if request.query_params.get('type_vaccine')  else None
        date_start = request.query_params.get('date_start') if request.query_params.get('date_start')  else None
        date_end = request.query_params.get('date_end') if request.query_params.get('date_end')  else None

        allEmployee = getAll()
        
        if state:
            allEmployee = getByStatusVaccination(allEmployee,state)
        
        if type_vaccine:
            allEmployee = getByTypeVaccine(allEmployee,type=type_vaccine)
        
        if date_start and date_end:
            allEmployee = getByDateRange(allEmployee,date_start,date_end)
        
        data = EmployeeSerializer(allEmployee,many=True)
        return Response(data.data,status=status.HTTP_200_OK)



class CreateEmployee(APIView):
    permission_classes = [UserPermission, IsAuthenticated]
    permission_required = 'core.add_employee'
    model = Employee


    class CreateEmployeeSerializer(Serializer):
        identification = CharField(required=True,validators=[UniqueValidator(queryset=Employee.objects.all()),NumericValidator()])
        name = CharField(required=True)
        last_name = CharField(required=True)
        email = EmailField(required=True)  


    
    @swagger_auto_schema(
        tags=["Empleados"],
        operation_summary="Crear un Empleados",
        
        request_body=CreateEmployeeSerializer(),
        responses={
            200: ResponseSerializer(),
        }
    )
    def post(self,request):
        data = self.CreateEmployeeSerializer(data=request.data)
        if data.is_valid():
            try:
                employee=create_employee(data.data)
                current_site = get_current_site(request=request).domain
                user = create_user({
                    'username':employee.identification,
                    'email':employee.email,
                    'first_name':employee.name,
                    'last_name':employee.last_name},current_site)
                employee.user = user
                employee.save()
                message = ResponseSerializer({"message":"Employee Created","type":"SUCCESS"})
                return Response(message.data,status=status.HTTP_201_CREATED)
            except Exception as e:
                message = ResponseSerializer({"message":e.__str__(),"type":"SERVER_ERROR"})
                return Response(message.data,status=status.HTTP_400_BAD_REQUEST)
        else:
            m = ""
            for i in data._errors.keys():
                m += i + " "+data._errors[i][0]+" "
            message = ResponseSerializer({"message":m,"type":"INVALID_FORMAT"})
            return Response(message.data,status=status.HTTP_400_BAD_REQUEST)
    


class UpdateEmployee(APIView):
    permission_classes = [UserPermission,IsAuthenticated]
    permission_required = 'core.change_employee'
    model = Employee

    class UpdateEmployeeSerializer(Serializer):
        birth_date = DateField()
        address = CharField()
        phone = CharField()
        is_vaccinated = BooleanField(validators=[RequiredConditional(fields=['type_vaccine','date_vaccine','number_doses'])])
        type_vaccine = CharField(required=False)
        date_vaccine = DateField(required=False)
        number_doses = IntegerField(required=False)



    @swagger_auto_schema(
        tags=["Empleados"],
        operation_summary="Actualiza un Empleados",
        
        request_body=UpdateEmployeeSerializer(),
        responses={
            200: EmployeeSerializer(many=True),
        }
    )
    def put(self,request,pk):
        data = self.UpdateEmployeeSerializer(data=request.data)
        if data.is_valid():
            try:

                employee = getById(pk)
                update_employee(employee,data.data)
                message = ResponseSerializer({"message":"Employee Updated","type":"SUCCESS"})
                return Response(message.data,status=status.HTTP_200_OK)
            except Exception as e:
                message = ResponseSerializer({"message":e.__str__(),"type":"NOT_FOUND"})
                return Response(message.data,status=status.HTTP_400_BAD_REQUEST)

        else:
            m = ""
            for i in data._errors.keys():
                m += i + " "+data._errors[i][0]+" "
            message = ResponseSerializer({"message":m,"type":"INVALID_FORMAT"})

            return Response(message.data,status=status.HTTP_400_BAD_REQUEST)


class GetEmployeebyUser(APIView):
    permission_classes = [IsAuthenticated]
    permission_required = 'core.change_employee'
    model = Employee



    
    @swagger_auto_schema(
        tags=["Empleados"],
        operation_summary="Obtiene el Empleado que esta en session",
        
        responses={
            200: EmployeeSerializer(),
        }
    )
    def get(self,request):
        user = request.user
        data = getByUserId(user.pk)
        res = EmployeeSerializer(data)
        return Response(res.data,status=status.HTTP_200_OK)



class UpdateEmployeebyUser(APIView):
    permission_classes = [IsAuthenticated]
    permission_required = 'core.change_employee'
    model = Employee




    class UpdateEmployeeByUserSerializer(Serializer):
        birth_date = DateField()
        address = CharField()
        phone = CharField()
        is_vaccinated = BooleanField(validators=[RequiredConditional(fields=['type_vaccine','date_vaccine','number_doses'])])
        type_vaccine = CharField(required=False)
        date_vaccine = DateField(required=False)
        number_doses = IntegerField(required=False)

    
    @swagger_auto_schema(
        tags=["Empleados"],
        operation_summary="Actualiza el Empleado que esta en session",
        
        request_body=UpdateEmployeeByUserSerializer(),
        responses={
            200: ResponseSerializer(),
        }
    )
    def put(self,request):
        user = request.user

        data = self.UpdateEmployeeByUserSerializer(data=request.data)
        if data.is_valid():
            try:
                print(user.pk)
                employee = getByUserId(user.pk)
                update_employee(employee,data.data)
                message = ResponseSerializer({"message":"Employee Updated","type":"SUCCESS"})
                return Response(message.data,status=status.HTTP_200_OK)
            except Exception as e:
                message = ResponseSerializer({"message":e.__str__(),"type":"NOT_FOUND"})
                return Response(message.data,status=status.HTTP_400_BAD_REQUEST)

        else:
            m = ""
            for i in data._errors.keys():
                m += i + " "+data._errors[i][0]+" "
            message = ResponseSerializer({"message":m,"type":"INVALID_FORMAT"})

            return Response(message.data,status=status.HTTP_400_BAD_REQUEST)



class DeleteEmployee(APIView):
    model = Employee
    permission_classes = [IsAuthenticated,UserPermission]
    permission_required = 'core.delete_employee'

    
    @swagger_auto_schema(
        tags=["Empleados"],
        operation_summary="Actualiza un Empleados",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER),

        ],
        responses={
            200: EmployeeSerializer(many=True),
        }
    )
    def delete(self,request,pk):
        employee = getById(pk)
        delete_user_by_id(employee.user.pk)
        delete_by_id(pk)
        message = ResponseSerializer({"message":"Employee Updated","type":"SUCCESS"})
        return Response(message.data,status=status.HTTP_200_OK)



class PasswordResetView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomPasswordResetSerializer


    @swagger_auto_schema(
        tags=["password"],
        operation_summary="Actualiza un Empleados",
        request_body=CustomPasswordResetSerializer(),
        responses={
            200: ResponseSerializer(),
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Password reset e-mail has been sent.','type':'SUCCESS'}, status=200, headers={'Access-Control-Allow-Origin': '*'})
        return Response(serializer.errors, status=400, headers={'Access-Control-Allow-Origin': '*'})