
from rest_framework.views import APIView, Response, status
from django.contrib.auth.models import User, Group, Permission
from rest_framework.serializers import ModelSerializer,CharField,PrimaryKeyRelatedField, EmailField,\
    Serializer,DateField,BooleanField, IntegerField,SlugRelatedField
from rest_framework.permissions import IsAuthenticated

from core.service.group import create_group, getAllGroups
from core.shared.permissions import UserPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.shared.serializer import ResponseSerializer


class CreateRole(APIView):
    model = Group
    permission_classes = [UserPermission, IsAuthenticated]
    permission_required = 'auth.add_group'

    class CreateRoleSerializer(ModelSerializer):
        permissions = SlugRelatedField(
            many=True,
            read_only=False,
            slug_field='codename',
            queryset= Permission.objects.all(),
            
        )
        class Meta:
            model = Group
            fields = '__all__'



    @swagger_auto_schema(
            tags=["Roles"],
            operation_summary="Crear Rol",
            request_body=CreateRoleSerializer(),
            responses={
                200: ResponseSerializer(),
            }
    )
    def post(self,request):
        data = self.CreateRoleSerializer(data=request.data)
        if data.is_valid():
            try:
                create_group(data)
                message = ResponseSerializer({"message":"Role Created","type":"SUCCESS"})
                return Response(message.data,status=status.HTTP_201_CREATED)
            except Exception as e:
                message = ResponseSerializer({"message":e.__str__(),"type":"SERVER_ERROR"})
                return Response(message.data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            m = ""
            for i in data._errors.keys():
                m += i + " "+data._errors[i][0]+" "
            message = ResponseSerializer({"message":m,"type":"INVALID_FORMAT"})
            return Response(message.data,status=status.HTTP_400_BAD_REQUEST)






class GetAllGroup(APIView):

    model = Group
    permission_classes = [IsAuthenticated,UserPermission]
    permission_required = 'auth.view_group'

    class GroupSerializer(ModelSerializer):
        permissions = SlugRelatedField(
            many=True,
            read_only=True,
            slug_field='codename',
            
        )
        class Meta:
            model = Group
            fields = '__all__'
    @swagger_auto_schema(
            tags=["Roles"],
            operation_summary="Listar Roles",
            responses={
                200: GroupSerializer(many=True),
            }
    )
    def get(self,request):
        data = getAllGroups()
        res = self.GroupSerializer(data,many=True)
        return Response(res.data,status=status.HTTP_200_OK)




class GetAllPermissions(APIView):
    model = Permission
    permission_classes = [IsAuthenticated,UserPermission]
    permission_required = ''



    class PermissionSerializer(ModelSerializer):
        class Meta:
            model = Permission
            fields = '__all__'

    
    @swagger_auto_schema(
            tags=["Permisos"],
            operation_summary="Listar Permisos",
            responses={
                200: PermissionSerializer(many=True),
            }
    )

    def get(self,request):
        data = self.model.objects.all();
        res = self.PermissionSerializer(data,many=True)
        return Response(res.data,status=status.HTTP_200_OK)
