from pytest import mark
from architecture.code_analysis_v3.core.gss import GSS
from architecture.code_analysis_v3.core.student import (
    StudentApproved,
    AbstractStudent,
    StudentInProgress,
)


@mark.skip
class TestNotifyGSS:
    def test_student_gss_notification_set_state_to_approved_when_all_subjects_approved(
        self, student_approved: AbstractStudent
    ):
        assert isinstance(student_approved.state, StudentApproved)
        assert student_approved.gpa == 9

    def test_student_gss_notification_keep_state_inprogress_when_any_subject_failed(
        self, student_in_progress: AbstractStudent
    ):
        first_subject = student_in_progress.subjects_in_progress[0]
        gss = GSS()
        # grade < 7 is failed
        gss.set_(3, first_subject, student_in_progress)
        student_in_progress.notify_me_about_gss(gss)
        assert isinstance(student_in_progress.state, StudentInProgress)
