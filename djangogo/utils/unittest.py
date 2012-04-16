"""Remember, unittests are WHAT not HOW"""

from django.utils.unittest import *

"""TODO:"""
"""-add useless keyword test to DesignTestCase, i.e. max_length on an integer"""
"""-separate out test_formats in DesignTestCase"""
"""-replace exec() with getattr"""
"""-unicode function test in DesignTestCase"""

class DesignTestCase(TestCase):

    unique_fields = ()
    nullable_fields = ()
    blankable_fields = ()

    """Syntax is (field name, format, positive_only (only for numerical))"""
    """This and above could be replaced with model_design"""
    field_formats = ()

    def tearDown(self):
        self.testmodel.delete()



    """format tests"""
    def test_formats(self):
        """Tests that each field is in the correct format"""
        """Each of these tests could be isolate to their own test"""

        for field_format in self.field_formats:
            field, format, positive_only = field_format

            field_type = self.testmodel._meta.get_field(field).get_internal_type()

            if "." not in format and "D" in format:
                FORMAT_TYPE = "integer"
            elif "." in format and "D" in format:
                FORMAT_TYPE = "decimal"
            elif "C" in format:
                FORMAT_TYPE = "character"

            """format test"""
            """checks fields support the correct formats"""
            if FORMAT_TYPE == "integer":
                test_format = int(format.replace("D", "9"))
            elif FORMAT_TYPE == "decimal":
                test_format = float(format.replace("D", "9"))
            elif FORMAT_TYPE == "character":
                test_format = "'%s'" % format

            exec("self.testmodel.%s = %s" % (field, test_format)) #bit hacky but it works
            #try this instead: setattr(self.testmodel,field,test_format)

            try:
                self.testmodel.save()
            except Exception, e:
                raise(AssertionError("%s field should support format %s" % (field, format)))

            """max_length test"""
            """done by comparing length to max_length"""
            """cannot be done by injection as this is tested at runtime"""
            if field_type == "CharField":
                if len(format) > self.testmodel._meta.get_field(field).max_length:
                    raise(AssertionError("%s field should support format %s" % (field, format)))


            """Check if small int would be preferable if not already used"""
            if FORMAT_TYPE == "integer":
                if len(format) < 5 and "SmallIntegerField" not in field_type:
                    raise(AssertionError("%s should be a SmallInteger" % field))
                if len(format) >= 5 and "SmallIntegerField" in field_type:
                    raise(AssertionError("%s is too large for a SmallInteger (not strictly true, not tested for values over 9999)" % field))


            """test if max_length could be smaller (injection)"""
            """done by injection, not valid for integers or characters"""
            if FORMAT_TYPE != "integer" and FORMAT_TYPE != "character":
                if FORMAT_TYPE == "integer":
                    test_format = int(format.replace("D", "9") + "9")
                elif FORMAT_TYPE == "decimal":
                    test_format = float(format.replace("D", "9") + "9")
                elif FORMAT_TYPE == "character":
                    test_format = "'%s'" % (format + "C")

                #Test by injection
                exec("self.testmodel.%s = %s" % (field, test_format)) #bit hacky but it works

                try:
                    self.testmodel.save()
                except Exception, e:
                    pass
                else:
                    raise(AssertionError("%s could be smaller" % (field)))

            """test if max_length could be smaller (comparison)"""
            """done by comparing length to max_length attribute, only used for characters"""
            if field_type == "CharField":
                if len(format) < self.testmodel._meta.get_field(field).max_length:
                    raise(AssertionError("%s could be smaller" % (field)))
                

            """positive_only test, only valid for integers"""
            """tested by attribute comparison"""
            if FORMAT_TYPE == "integer":
                """
                Cannot test as would like to as django tests if positive during admin panel. Original code:

                test_format = 0 - int(format.replace("D", "9"))
                exec("self.testmodel.%s = %s" % (field, test_format)) #bit hacky but it works
                try:
                    self.testmodel.save()
                except Exception, e:
                    if not positive_only: raise(AssertionError("%s should support negative values" % field))
                else:
                    if positive_only: raise(AssertionError("%s should NOT support negative values %s" % (field, test_format)))
                """

                if positive_only and "Positive" not in field_type:
                    raise(AssertionError("%s should use a Positive only field" % (field)))
                elif not positive_only and "Positive" in field_type:
                    raise(AssertionError("%s should NOT be using a Positive only field" % (field)))
        
            self.tearDown()
            self.setUp()

    """Attribute tests"""
    def test_uniqueness(self):
        """Tests that each variable that should be unique, is unique"""
        for field in self.testmodel._meta.fields:
            if field.name in self.unique_fields or field.name == "id":
                if not field.unique:
                    raise(AssertionError("%s is not unique" % (field.name)))
            else:
                if field.unique:
                    raise(AssertionError("%s is unique" % (field.name)))

            self.tearDown()
            self.setUp()

    def test_nullable(self):
        """Test whether fields specified as nullable are nullable"""      
        for field in self.testmodel._meta.fields:
            if field.name in self.nullable_fields:
                if not field.null:
                    raise(AssertionError("%s is not nullable" % (field.name)))
            else:
                if field.null:
                    raise(AssertionError("%s is nullable" % (field.name)))

            self.tearDown()
            self.setUp()

    def test_blankable(self):
        """Test blankable fields"""
        for field in self.testmodel._meta.fields:
            if field.name in self.blankable_fields or field.name == "id":
                if not field.blank:
                    raise(AssertionError("%s is not blankable" % (field.name)))
            else:
                if field.blank:
                    raise(AssertionError("%s is blankable" % (field.name)))

            self.tearDown()
            self.setUp()