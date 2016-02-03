from sqlalchemy import event
from nautilus.network import dispatchAction

class CRUDNotificationCreator:

    nautilus_base = True

    @classmethod
    def onCreation(cls):
        # perform the intended behavior
        super().onCreation()
        # add the event listeners
        cls.addEventCreators()

    @classmethod
    def addEventCreators(cls):
        """ Adds the event creators to the class record """

        # on save, send an action with type <model>_created
        @event.listens_for(cls, 'after_insert')
        def dispatchSaveAction(mapper, connection, target):
            """ notifies the network of the new user model """
            dispatchAction({
                'type': 'user_created',
                'payload': target.__json__(),
            })
