# external imports
import unittest
from unittest.mock import Mock
# local imports
import nautilus
import nautilus.models as models
import nautilus.network.events.actionHandlers as action_handlers
from ..util import async_test, Mock, MockModel

class TestUtil(unittest.TestCase):

    def setUp(self):
        # point the database to a in-memory sqlite database
        nautilus.database.init_db('sqlite:///test.db')

        # save the class record
        self.model = MockModel()
        # create the table in the database
        nautilus.db.create_table(self.model)


    def tearDown(self):
        nautilus.db.drop_table(self.model)


    @async_test
    async def test_create_action_handler(self):
        # create a `create` action handler
        action_handler = action_handlers.create_handler(self.model)
        # the action type to fire the
        action_type = nautilus.conventions.actions.get_crud_action('create', self.model)
        # the attributes for the new Model
        payload = dict(name = 'foo')

        # the query for the number of matching records
        record_query = self.model.select().where(self.model.name=='foo')

        # the number of matching records before we trigger the handler
        assert record_query.count() == 0
        # call the action handler
        await action_handler(Mock(), action_type=action_type, payload=payload, props={}, notify=False)

        # make sure there is now a matching record
        assert record_query.count() == 1, (
            "Record was not created by action handler"
        )
        assert record_query[0].name == 'foo', (
            "Record did not have the correct attribute value"
        )


    @async_test
    async def test_delete_action_handler(self):
        # create a record in the test database
        record = self.model(name='foo')
        # save the record
        record.save()

        # create a `create` action handler
        action_handler = action_handlers.delete_handler(self.model)
        # the action type to fire the
        action_type = nautilus.conventions.get_crud_action('delete', self.model)
        # the attributes for the new Model
        payload = record.id

        # the query for the number of matching records
        record_query = self.model.select().where(self.model.id==record.id)
        # fire the action handler
        await action_handler(Mock(), action_type=action_type, payload=payload, props={}, notify=False)
        # make sure there aren't any queries
        assert record_query.count() == 0, (
            "There were records matching query after it shoudl have been removed."
        )


    @async_test
    async def test_update_action_handler(self):
        # create a record in the test database
        record = self.model(name='foo')
        # save the record
        record.save()
        # the query to grab the model we changed
        record_query = self.model.select().where(self.model.id == 1)
        # make sure the record was saved and is retrievable
        assert record_query.get().name == 'foo'

        # create a `create` action handler
        action_handler = action_handlers.update_handler(self.model)
        # the action type to fire the
        action_type = nautilus.conventions.get_crud_action('update', self.model)

        # the attributes for the new Model
        payload = dict(id=record.id, name='bar')

        # fire the action handler
        await action_handler(Mock(), action_type=action_type, payload=payload, props={}, notify=False)

        # make sure the record was changed
        assert record_query.get().name == 'bar', (
            "Model query was not updated."
        )
