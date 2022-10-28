from clip.storage.base import BaseStorage
import json
import os


class JsonStorage(BaseStorage):
    values = {}
    filename = os.path.join(os.path.expanduser('~'), '.clip')

    def bootstrap(self):
        try:
            file = open(self.filename, 'r')
            self.values = json.loads(file.read())
            file.close()
        except Exception:
            file = open(self.filename, 'w+')
            file.write('{}')
            file.flush()
            file.close()

    def save(self):
        file = open(self.filename, 'w+')
        file.write(json.dumps(self.values))
        file.flush()
        file.close()

    def __unicode__(self):
        return 'Json Storage'
