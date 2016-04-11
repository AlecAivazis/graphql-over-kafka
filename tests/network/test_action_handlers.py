# external imports
import unittest
from unittest.mock import MagicMock
# local imports
import nautilus
import nautilus.models as models
import nautilus.network.amqp.actionHandlers as action_handlers

class TestUtil(unittest.TestCase):

    def setUp(self):
        # point the database to a in-memory sqlite database
        nautilus.database.init_db('sqlite:///test.db')

        # the model to test
        class ActionHandlerTestModel(models.BaseModel):
            first_name = models.fields.CharField()

        # save the class record
        self.model = ActionHandlerTestModel
        # create the table in the database
        nautilus.db.create_table(self.model)


    def tearDown(self):
        nautilus.db.drop_table(self.model)


    def test_create_action_handler(self):
        # create a `create` action handler
        action_handler = action_handlers.create_handler(self.model)
        # the action type to fire the
        action_type = nautilus.conventions.actions.get_crud_action('create', self.model)
        # the attributes for the new Model
        payload = dict(first_name = 'foo')

        # the query for the number of matching records
        record_query = self.model.select().where(self.model.first_name=='foo')

        # the number of matching records before we trigger the handler
        assert record_query.count() == 0
        # call the action handler
        action_handler(action_type, payload, dispatcher=MagicMock())
        # make sure there is now a matching record
        assert record_query.count() == 1, (
            "Record was not created by action handler"
        )
        assert record_query[0].first_name == 'foo', (
            "Record did not have the correct attribute value"
        )


    def test_delete_action_handler(self):
        # create a record in the test database
        record = self.model(first_name='foo')
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
        action_handler(action_type, payload, dispatcher=MagicMock())
        # make sure there aren't any queries
        assert record_query.count() == 0, (
            "There were records matching query after it shoudl have been removed."
        )


    def test_update_action_handler(self):
        # create a record in the test database
        record = self.model(first_name='foo')
        # save the record
        record.save()
        # the query to grab the model we changed
        record_query = self.model.select().where(self.model.id == 1)
        # make sure the record was saved and is retrievable
        assert record_query.get().first_name == 'foo'

        # create a `create` action handler
        action_handler = action_handlers.update_handler(self.model)
        # the action type to fire the
        action_type = nautilus.conventions.get_crud_action('update', self.model)

        # the attributes for the new Model
        payload = dict(id=record.id, first_name='bar')

        # fire the action handler
        action_handler(action_type, payload, dispatcher=MagicMock())

        # make sure the record was changed
        assert record_query.get().first_name == 'bar', (
            "Model query was not updated."
        )
