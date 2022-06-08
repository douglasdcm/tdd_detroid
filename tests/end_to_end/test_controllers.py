from src.controller import StudentController


class TestController:

    def test_save_student_details(self):
        score = 3
        id_ = 2
        controller = StudentController()
        controller.save()
        controller.save()
        controller.save()
        controller.set_score(id_, score)

        assert controller.get_score(id_) == score
