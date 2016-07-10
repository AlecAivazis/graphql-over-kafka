# external imports
import unittest
# local imports
import nautilus
import nautilus.models as models
from nautilus.api.filter import args_for_model, filter_model
from ..util import MockModel

class TestUtil(unittest.TestCase):

    def setUp(self):
        # point the database to a in-memory sqlite database
        nautilus.database.init_db('sqlite:///test.db')

        # save a reference to the test model
        self.model = MockModel()
        # generate the arguments for the model
        self.args = args_for_model(self.model)
        # create a set out of the arguments
        self.arg_names = set(self.args.keys())

        # create a database table to test on
        self.model.create_table()

        # generate test data
        self._gen_testdata()


    def tearDown(self):
        # remove the test table
        self.model.drop_table()


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
        contains_filter_args = {'name_in', 'date_in'}
        # make sure the arguments exist for the contains filter
        assert self.arg_names >= contains_filter_args, (
            "Generated args do not have contains filter."
        )


    def test_can_filter_by_field(self):
        # the argument to filter for
        filter_args = dict(name='foo1')
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # make sure only one record was returned
        assert len(records_filtered) == 1, (
            "More than one record was returned by filter."
        )

        # pull out the retrieved record
        retrieved_record_name = records_filtered[0].name
        # make sure the first name matches
        expected = 'foo1'
        assert retrieved_record_name == expected, (
            "Got %(retrieved_record_name)s instead of %(expected)s" % locals()
        )


    def test_can_filter_by_contains(self):
        # the argument to filter for
        filter_args = dict(name_in=['foo1', 'foo2'])
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # make sure only one record was returned
        assert len(records_filtered) == 2, (
            "More than one record was returned by filter."
        )

        # figure out the names of the records we retrieved
        retrieved_names = {record.name for record in records_filtered}

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
        retrieved_names = [record.name for record in records_filtered]
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
        retrieved_names = [record.name for record in records_filtered]
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
        retrieved_names = [record.name for record in records_filtered]
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
        retrieved_names = [record.name for record in records_filtered]
        expected = ['foo2', 'bar2', 'foo3', 'bar3']
        assert retrieved_names == expected, (
            "Got %(retrieved_names)s instead of %(expected)s" % locals()
        )


    def test_can_handle_first_offset_order_by(self):
        # the argument to filter for
        filter_args = dict(first=4, offset=2, order_by=["date", "-name"])
        # filter the models
        records_filtered = filter_model(self.model, filter_args)

        # figure out the names of the records we retrieved
        retrieved_names = [record.name for record in records_filtered]
        expected = ['foo7', 'foo6', 'foo5', 'foo4']
        assert retrieved_names == expected, (
            "Got %(retrieved_names)s instead of %(expected)s" % locals()
        )


    def _gen_testdata(self):
        # some test records
        for i in range(10):
            self.model(name='foo%s' % (i+1), date='bar').save()
            self.model(name='bar%s' % (i+1), date='foo').save()
