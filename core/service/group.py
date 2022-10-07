

from django.contrib.auth.models import User, Group, Permission


def create_group(data):
    group = Group.objects.create(name=data.get('name'))
    for i in data.get('permissions'):
        per = Permission.objects.filter(codename=i.get('codename')).last()
        group.permissions.add(per.id)
    return group



def getAllGroups():
    return Group.objects.all()