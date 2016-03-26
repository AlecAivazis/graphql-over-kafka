# external imports
import unittest
import graphene.core.types.scalars as graphene
# local imports
import nautilus.models.fields as nautilus
from nautilus.contrib.graphene_peewee import convert_peewee_field



class TestUtil(unittest.TestCase):

    def assert_field_converted(self, nautilus_field, graphene_field):
        # convert the nautilus field to the corresponding graphene type
        test_graphene_type = convert_peewee_field(nautilus_field)
        # make sure the converted type matches the graphene field
        assert isinstance(test_graphene_type, graphene_field), (
            "nautilus field was not properly coverted to %s" % graphene_field.__class__
        )


    def test_can_convert_BigIntegerField(self):
        self.assert_field_converted(nautilus.BigIntegerField(), graphene.Int)

    def test_can_convert_BooleanField(self):
        self.assert_field_converted(nautilus.BooleanField(), graphene.Boolean)

    def test_can_convert_CharField(self):
        self.assert_field_converted(nautilus.CharField(), graphene.String)

    def test_can_convert_DateField(self):
        self.assert_field_converted(nautilus.DateField(), graphene.String)

    def test_can_convert_DateTimeField(self):
        self.assert_field_converted(nautilus.DateTimeField(), graphene.String)

    def test_can_convert_DecimalField(self):
        self.assert_field_converted(nautilus.DecimalField(), graphene.Float)

    def test_can_convert_DoubleField(self):
        self.assert_field_converted(nautilus.DoubleField(), graphene.Float)

    def test_can_convert_FixedCharField(self):
        self.assert_field_converted(nautilus.FixedCharField(), graphene.String)

    def test_can_convert_FloatField(self):
        self.assert_field_converted(nautilus.FloatField(), graphene.Float)

    def test_can_convert_IntegerField(self):
        self.assert_field_converted(nautilus.IntegerField(), graphene.Int)

    def test_can_convert_PrimaryKeyField(self):
        self.assert_field_converted(nautilus.PrimaryKeyField(), graphene.ID)

    def test_can_convert_TextField(self):
        self.assert_field_converted(nautilus.TextField(), graphene.String)

    def test_can_convert_TimeField(self):
        self.assert_field_converted(nautilus.TimeField(), graphene.String)

    def test_can_convert_UUIDField(self):
        self.assert_field_converted(nautilus.UUIDField(), graphene.String)

    # def test_can_convert_ForeignKeyField(self):
    #     self.assert_field_converted(nautilus.ForeignKeyField, graphene.ID)

    # def test_can_convert_BareField(self):
    #     self.assert_field_converted(nautilus.BareField, graphene)

    # def test_can_convert_BlobField(self):
    #     self.assert_field_converted()

