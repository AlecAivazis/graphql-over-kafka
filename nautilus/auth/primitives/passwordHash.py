# from: http://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy

import bcrypt

class PasswordHash:
    """ This is a wrapper class over password hashes that abstracts equality """

    def __init__(self, hash_, rounds=None):
        # make sure the hash is valid
        if len(hash_) != 60:
            raise ValueError('bcrypt hash should be 60 chars.')
        elif hash_.count('$'.encode('utf-8')) != 3:
            raise ValueError('bcrypt hash should have 3x "$".')

        # save the required instance variables
        self.hash = hash_
        # figure out the current strength based on the saved hash
        self.rounds = int(str(self.hash).split('$')[2])
        # the intended number of rounds (in case there is an upgrade)
        self.desired_rounds = rounds or self.rounds


    # this allows us to easily check if a candidate password matches the hash
    # using: hash == 'foo'
    def __eq__(self, candidate):
        """Hashes the candidate string and compares it to the stored hash."""

        if isinstance(candidate, str):
            # convert it to a byte string
            candidate = candidate.encode('utf-8')

        # if the candidate matches the saved hash
        if self.hash == bcrypt.hashpw(candidate, self.hash):
            # if the computed number of rounds is less than the designated one
            if self.rounds < self.desired_rounds:
                # rehash the password
                self.rehash(candidate)

            return True
        # otherwise the password doesn't match
        else:
            return False


    def __repr__(self):
        """Simple object representation."""
        return '<{}: {}>'.format(type(self).__name__, self.hash)


    @classmethod
    def new(cls, password, rounds):
        """Creates a PasswordHash from the given password."""
        if isinstance(password, str):
            password = password.encode('utf-8')
        return cls(cls._new(password, rounds))


    @classmethod
    def coerce(cls, key, value):
        """Ensure that loaded values are PasswordHashes."""
        if isinstance(value, PasswordHash):
            return value
        return super(PasswordHash, cls).coerce(key, value)


    @staticmethod
    def _new(password, rounds):
        """
            Returns a new bcrypt hash for the given password and rounds.
            note: Implemented to reduce repitition in `new` and `rehash`.
        """
        return bcrypt.hashpw(password, bcrypt.gensalt(rounds))


    def rehash(self, password):
        """Recreates the internal hash."""
        self.hash = self._new(password, self.desired_rounds)
        self.rounds = self.desired_rounds
