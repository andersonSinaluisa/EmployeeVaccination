from django.urls import path
from .views.employee import CreateEmployee, UpdateEmployee, GetEmployee, GetEmployeebyUser,\
    DeleteEmployee,UpdateEmployeebyUser,PasswordResetView
from .views.group import CreateRole,GetAllGroup,GetAllPermissions
from .views.vaccine import CreateVaccine,GetAllVaccine
from rest_auth.views import (
    PasswordResetConfirmView,
    PasswordChangeView,
    LogoutView
)


urlpatterns = [
    path('employee/list/', GetEmployee.as_view(), name='visit_list'),
    path('employee/', GetEmployeebyUser.as_view(), name='visit_list'),
    path('employee/update/<int:pk>', UpdateEmployee.as_view(), name='visits_create'),
    path('employee/update_by_session/', UpdateEmployeebyUser.as_view(), name='visits_create'),
    path('employee/create/', CreateEmployee.as_view(), name='visit_update'),
    path('employee/delete/<int:pk>',DeleteEmployee.as_view(),name='visits_generate_report'),

    path('role/create/', CreateRole.as_view(), name='role_create'),
    path('role/list/', GetAllGroup.as_view(), name='role_list'),

    path('permission/list/', GetAllPermissions.as_view(), name='permission_list'),


    path('vaccine/create/', CreateVaccine.as_view(), name='permission_list'),
    path('vaccine/list/', GetAllVaccine.as_view(), name='permission_list'),
    path('password/reset/', PasswordResetView.as_view()),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(),
        name='rest_password_change'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),


]
