class IDMixin(object):

    @property
    def id(self):
        return self.key.id()