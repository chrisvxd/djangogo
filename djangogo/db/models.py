import datetime
from django.db.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class GenericModel(Model):
    #Can be related to any other model
    content_type = ForeignKey(ContentType)
    object_id = PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    class Meta:
        abstract = True


# class MultiSelectFormField(forms.MultipleChoiceField):
#     """Sourced from http://djangosnippets.org/snippets/1200/"""
#     widget = forms.CheckboxSelectMultiple

#     def __init__(self, *args, **kwargs):
#         self.max_choices = kwargs.pop('max_choices', 0)
#         super(MultiSelectFormField, self).__init__(*args, **kwargs)

#     def clean(self, value):
#         if not value and self.required:
#             raise forms.ValidationError(self.error_messages['required'])
#         if value and self.max_choices and len(value) > self.max_choices:
#             raise forms.ValidationError('You must select a maximum of %s choice%s.'
#                     % (apnumber(self.max_choices), pluralize(self.max_choices)))
#         return value

# class MultiSelectField(Field):
#     """Sourced from http://djangosnippets.org/snippets/1200/"""

#     __metaclass__ = SubfieldBase
    
#     def get_internal_type(self):
#         return "CharField"

#     def get_choices_default(self):
#         return self.get_choices(include_blank=False)

#     def _get_FIELD_display(self, field):
#         value = getattr(self, field.attname)
#         choicedict = dict(field.choices)

#     def formfield(self, **kwargs):
#         # don't call super, as that overrides default widget if it has choices
#         defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name), 
#                     'help_text': self.help_text, 'choices':self.choices}
#         if self.has_default():
#             defaults['initial'] = self.get_default()
#         defaults.update(kwargs)
#         return MultiSelectFormField(**defaults)

#     def get_db_prep_value(self, value):
#         if isinstance(value, basestring):
#             return value
#         elif isinstance(value, list):
#             return ",".join(value)

#     def to_python(self, value):
#         if isinstance(value, list):
#             return value
#         return value.split(",")

#     def contribute_to_class(self, cls, name):
#         super(MultiSelectField, self).contribute_to_class(cls, name)
#         if self.choices:
#             func = lambda self, fieldname = name, choicedict = dict(self.choices):",".join([choicedict.get(value,value) for value in getattr(self,fieldname)])
#             setattr(cls, 'get_%s_display' % self.name, func)


# Old integer time fields. Replaced by admin panel JS and DateTimeField()
#
# class YearField(PositiveIntegerField):
#     def tuplify(x): return (x,x)
#     choices = map(tuplify, range(1930, datetime.datetime.now().year + 1))
# 
# class MonthField(PositiveIntegerField):
#     def tuplify(x): return (x,x)
#     choices = map(tuplify, range(1,13))
#
# class YearlyRangeTimeSlot(GenericModel):
#     from_year = YearField(null=True,blank=True)
#     to_year = YearField()
# 
#     class Meta:
#         abstract = True  
# 
# class MonthlyRangeTimeSlot(GenericModel):
#     from_year = YearField(null=True,blank=True)
#     from_month = MonthField(null=True,blank=True)
#     to_year = YearField(null=True,blank=True)
#     to_month = MonthField(null=True,blank=True)
# 
#     class Meta:
#         abstract = True  
# 
# class YearlyTimeSlot(GenericModel):
#   year = YearField(null=True,blank=True)
# 
#   class Meta:
#       abstract = True  
# 
# class MonthlyTimeSlot(GenericModel):
#   year = YearField(null=True,blank=True)
#   month = MonthField(null=True,blank=True)
# 
#   class Meta:
#       abstract = True  