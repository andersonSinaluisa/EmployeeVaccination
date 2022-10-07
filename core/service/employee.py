import datetime
from core.models import Employee,Vaccination,Vaccine
from core.service.vaccine import getVaccineByName



def create_employee(data:dict)->Employee:
    """
    Crea un empleado a partir de un diccionario de datos y devuelve el empleado si se creó con éxito, o
    Ninguno si no se creó.
    
    :param data: Estos son los datos con los que desea crear el empleado
    :type data: dict
    :return: Se está devolviendo un nuevo objeto de empleado.
    """
    return Employee.objects.create(**data)
    


def update_employee(data:dict,id:int)->Employee:
    """
    Actualiza al empleado con la identificación dada con los datos dados.
    
    :param data: Estos son los datos que desea actualizar
    :type data: dict
    :param id: El id del empleado a actualizar
    :type id: int
    :return: El objeto empleado está siendo devuelto.
    """
    try:
        employee = Employee.objects.get(id=id)
        employee.update(**data)
        return employee
    except Exception as e:
        return None



def delete_by_id(id:int):
    """
    > Eliminar el empleado con la identificación dada
    
    :param id: El id del empleado que desea eliminar
    :type id: int
    """
    Employee.objects.filter(id=id).delete()



def getAll():
    """
    Devuelve todos los empleados en la base de datos.
    :return: Todos los objetos de la tabla Empleado
    """
    return Employee.objects.all()


def getById(id:int):
    return Employee.objects.get(id=id)

def getByUserId(id:int):
    return Employee.objects.get(user_id=id)


def update_employee(employee,data):
    employee.birth_date = data.get('birth_date')
    employee.address = data.get('address')
    employee.phone = data.get('phone')
    employee.is_vaccinated = data.get('is_vaccinated')
    if data.get('is_vaccinated')==True:
        vaccine = getVaccineByName(data.get('type_vaccine'))
        Vaccination.objects.create(type=vaccine,number_doses=data.get('number_doses'),date=data.get('date_vaccine'),employee=employee)
    employee.save()


def getByStatusVaccination(employees,state:bool):
    """
    > Esta función devuelve una lista de empleados que están vacunados o no vacunados según el valor
    booleano pasado a la función
    
    :param state: bool
    :type state: bool
    :return: Una lista de empleados que han sido vacunados o no.
    """
    return employees.objects.filter(is_vaccinated=state)



def getByDateRange(employees,date_start:datetime,date_end:datetime):
    """
    Devuelve una lista de empleados que se han vacunado entre las dos fechas.
    
    :param date_start: la fecha de inicio del intervalo de fechas
    :type date_start: datetime
    :param date_end: La fecha de finalización del intervalo de fechas
    :type date_end: datetime
    :return: Una lista de empleados que han tenido una vacuna entre las dos fechas.
    """
    result = Vaccination.objects.filter(date__range=(date_start,date_end))
    employee_list = employees
    for i in result:
        employee = result.employee  
        if employee not in employee_list:
            employee_list.append(employee)

    return employee_list



def getByTypeVaccine(employees,type:str):
    """
    Toma una lista de empleados y un tipo de vacuna, y devuelve una lista de empleados que han sido
    vacunados con ese tipo de vacuna
    
    :param employees: lista de empleados
    :param type: tipo de vacuna
    :type type: str
    :return: Una lista de empleados que han sido vacunados con un tipo específico de vacuna.
    """
    result = Vaccination.objects.filter(type__type=type)
    employee_list = employees
    for i in result:
            employee = result.employee  
            if employee not in employee_list:
                employee_list.append(employee)

    return employee_list