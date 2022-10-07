from rest_framework.validators import qs_filter,qs_exists,ValidationError
from rest_framework.utils.representation import smart_repr
import re


class NumericValidator:
    
    message = 'This field must be numeric.'
    requires_context = True

    def __init__(self, message=None, lookup='exact'):
        self.message = message or self.message
        self.lookup = lookup



    def __call__(self, value, serializer_field):

        field_name = serializer_field.source_attrs[-1]
        instance = getattr(serializer_field.parent, 'instance', None)
        print(value)
        if not value.isdigit():
            raise ValidationError(self.message, code='unique')

            

    def __repr__(self):
        return '<%s()>' % (
            self.__class__.__name__,
        )



class RequiredConditional:
    message = "This field is required"
    requires_context = True
    fields = []

    def __init__(self, message=None, lookup='exact',fields=[]):
        self.message = message or self.message
        self.lookup = lookup
        self.fields = fields


    def __call__(self, value, serializer_field):

        field_name = serializer_field.source_attrs[-1]
        initial_data = getattr(serializer_field.parent, 'initial_data', None)
        if value==True:
            try:
                for i in self.fields:
                    initial_data[i]
            except Exception as e:
                self.message = "Fields {0} is required".format(", ".join(self.fields))
                raise ValidationError(self.message, code='unique')  

    def __repr__(self):
        return '<%s()>' % (
            self.__class__.__name__,
        )