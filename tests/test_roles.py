def test_just_student_role_can_take_subjects_to_course():
    class StudentRole:
        def take_subject(self, subject):
            return True

    role = StudentRole()
    assert role.take_subject("subject1") == True
