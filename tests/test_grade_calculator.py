from src.services.grade_calculator import GradeCalculator
from src.services.student_handler import StudentHandler
from src import utils


# def test_calculate_student_gpa_when_no_grades(set_in_memory_database):
#     gpa_handler = GPAHandler(set_in_memory_database)
#     student_identifier = utils.generate_student_identifier(
#         "any", "123.456.789-10", "any"
#     )
#     assert gpa_handler.calculate_for(student_identifier) == 0
