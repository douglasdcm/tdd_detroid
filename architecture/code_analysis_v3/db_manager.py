import pickle
from architecture.code_analysis_v3.core.base_object import NoneCoreObject


class BaseCoreDataManager:
    DATA_FILE: str = ""

    def save_object(self, app_object: object):
        with open(self.DATA_FILE, "ab") as outp:
            pickle.dump(app_object, outp, pickle.HIGHEST_PROTOCOL)

    def loadall(self):
        with open(self.DATA_FILE, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def load_by_nui(self, nui):
        for obj in self.loadall():
            # All AbstractCoreObjects has a `nui`
            if obj.nui == nui:
                return obj
        return NoneCoreObject()


class StudentDataManager(BaseCoreDataManager):
    DATA_FILE = "db/student.pickle"
