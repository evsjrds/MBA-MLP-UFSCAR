class Person(object):
    def __init__(self, uid, genre):
        self._uid = uid
        self._genre = genre

    def get_uid(self):
        return self._uid

    def get_genre(self):
        return self._genre
