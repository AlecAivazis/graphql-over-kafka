# external imports
import unittest
# local imports
import nautilus
import nautilus.models as models
from nautilus.api.filter import args_for_model, filter_model

class TestUtil(unittest.TestCase):

    def setUp(self):
        # point the database to a in-memory sqlite database
        nautilus.database.init_db('sqlite:///test.db')

        # the model to test
        class TestModel(models.BaseModel):
            first_name = models.fields.CharField()
            last_name = models.fields.CharField()

        # save a reference to the test model
        self.model = TestModel
        # generate the arguments for the model
        self.args = args_for_model(TestModel)
        # create a set out of the arguments
        self.arg_names = set(self.args.keys())

        # create a database table to test on
        nautilus.db.create_table(self.model)

        # generate test data
        self._gen_testdata()


    def tearDown(self):
        # remove the test table
        nautilus.db.drop_table(self.model)


    def test_args_match_model(self):
        # make sure the argument contain the model fields
        assert self.arg_names >= {field.name for field in self.model.fields()}, (
            "Generated args do not contain model fields"
        )


    def test_pk_filter(self): pass


    def test_pk_filter_with_custom_pk(self): pass


    def test_pk_in_filter(self): pass


    def test_args_has_oneof_filter(self):
        # the filters we would exepect for the contains arg
        contains_filter_args = {'first_name_in', 'last_name_in'}
        # make sure the arguments exist for the contains filter
        assert self.arg_names >= contains_filter_args, (
            "Generated args do not have contains filter."
        )


    def test_can_filter_by_field(self):
        # the argument to filter for
        filter_args = dict(first_name='foo1')
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # make sure only one record was returned
        assert len(records_filtered) == 1, (
            "More than one record was returned by filter."
        )

        # pull out the retrieved record
        retrieved_record_first_name = records_filtered[0].first_name
        # make sure the first name matches
        expected = 'foo1'
        assert retrieved_record_first_name == expected, (
            "Got %(retrieved_record_first_name)s instead of %(expected)s" % locals()
        )


    def test_can_filter_by_contains(self):
        # the argument to filter for
        filter_args = dict(first_name_in=['foo1', 'foo2'])
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # make sure only one record was returned
        assert len(records_filtered) == 2, (
            "More than one record was returned by filter."
        )

        # figure out the names of the records we retrieved
        retrieved_names = {record.first_name for record in records_filtered}

        # make sure the first name matches
        expected = {'foo1', 'foo2'}
        assert retrieved_names == expected, (
            "Got %(retrieved_names)s instead of %(expected)s" % locals()
        )


    def test_can_handle_first(self):
        # the argument to filter for
        filter_args = dict(first=2, offset=0)
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # figure out the names of the records we retrieved
        retrieved_names = [record.first_name for record in records_filtered]
        expected = ['foo1', 'bar1']
        assert retrieved_names == expected, (
            "Got %(retrieved_names)s instead of %(expected)s" % locals()
        )


    def test_can_handle_last(self):
        # the argument to filter for
        filter_args = dict(last=2, offset=0)
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # figure out the names of the records we retrieved
        retrieved_names = [record.first_name for record in records_filtered]
        expected = ['bar10', 'foo10']
        assert retrieved_names == expected, (
            "Got %(retrieved_names)s instead of %(expected)s" % locals()
        )


    def test_can_handle_last_offset(self):
        # the argument to filter for
        filter_args = dict(last=2, offset=2)
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # figure out the names of the records we retrieved
        retrieved_names = [record.first_name for record in records_filtered]
        expected = ['bar9', 'foo9']
        assert retrieved_names == expected, (
            "Got %(retrieved_names)s instead of %(expected)s" % locals()
        )


    def test_can_handle_first_offset(self):
        # the argument to filter for
        filter_args = dict(first=4, offset=2)
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # figure out the names of the records we retrieved
        retrieved_names = [record.first_name for record in records_filtered]
        expected = ['foo2', 'bar2', 'foo3', 'bar3']
        assert retrieved_names == expected, (
            "Got %(retrieved_names)s instead of %(expected)s" % locals()
        )


    def test_can_handle_first_offset_order_by(self):
        # the argument to filter for
        filter_args = dict(first=4, offset=2, order_by=["last_name", "-first_name"])
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # figure out the names of the records we retrieved
        retrieved_names = [record.first_name for record in records_filtered]
        expected = ['foo7', 'foo6', 'foo5', 'foo4']
        assert retrieved_names == expected, (
            "Got %(retrieved_names)s instead of %(expected)s" % locals()
        )


    def _gen_testdata(self):
        # some test records
        for i in range(10):
            self.model(first_name='foo%s' % (i+1), last_name='bar').save()
            self.model(first_name='bar%s' % (i+1), last_name='foo').save()
