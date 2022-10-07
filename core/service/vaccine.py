
from core.models import Vaccine


def getVaccineByName(name):
    return Vaccine.objects.get(type=name)


def create_vaccine(data):
    return Vaccine.objects.create(**data)



def get_all_vaccine():
    return Vaccine.objects.all()