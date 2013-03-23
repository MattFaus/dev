
class MyModel(ndb.Model):
    def create_or_update(key, data):
        """Returns True if entity was created or updated, False otherwise."""

        current = MyModel.get_or_insert(key, data=data)

        # How do I know if something was gotten or inserted?
        if(current.data != data)
            current.data = data
            return True

        return False
