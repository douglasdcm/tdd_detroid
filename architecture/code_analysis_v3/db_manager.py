import pickle
from core.student import NoneStudent
from core.subject import NoneSubject
from core.course import NoneCourse
from core.base_object import AbstractCoreObject

DB_FOLDER = "db/"
FILE_EXTENSION = ".pickle"


class BaseCoreDataManager:
    DATA_FILE: str = ""

    def _dump_data(self, app_object, outp):
        data = {f"{app_object.nui}": app_object}
        pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)

    def _get_none_object(self):
        raise NotImplementedError("To be implemented by sub-classes")

    def clear(self):
        with open(self.DATA_FILE, "wb"):
            pass

    def save_objects(self, app_objects: list[AbstractCoreObject]):
        with open(self.DATA_FILE, "ab") as outp:
            for app_object in app_objects:
                self._dump_data(app_object, outp)

    def save_object(self, app_object: object):
        with open(self.DATA_FILE, "ab") as outp:
            self._dump_data(app_object, outp)

    def update_object(self, app_object: AbstractCoreObject):
        result = []
        for obj in self.loadall():
            result.append(obj)
        with open(self.DATA_FILE, "wb") as outp:
            pass
        try:
            with open(self.DATA_FILE, "ab") as outp:
                for obj in result:
                    if obj.get(str(app_object.nui)):
                        self._dump_data(app_object, outp)
                        continue
                    pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
        except Exception:
            with open(self.DATA_FILE, "ab") as outp:
                for obj in result:
                    pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

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
            result = obj.get(str(nui))
            if result:
                return result
        return self._get_none_object()


class StudentDataManager(BaseCoreDataManager):
    DATA_FILE = f"{DB_FOLDER}student{FILE_EXTENSION}"

    def _get_none_object(self):
        return NoneStudent()


class SubjectDataManager(BaseCoreDataManager):
    DATA_FILE = f"{DB_FOLDER}subject{FILE_EXTENSION}"

    def _get_none_object(self):
        return NoneSubject()


class CourseDataManager(BaseCoreDataManager):
    DATA_FILE = f"{DB_FOLDER}course{FILE_EXTENSION}"

    def _get_none_object(self):
        return NoneCourse()
