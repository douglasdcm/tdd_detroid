#include "declarations.h"
#include "../unity.h"

void setUp(){}
void tearDown(){}

// 1. Each student will have a grade control called "grade point average" (GPA).
// 2. The GPA is the average of the student's grades in the ~~courses~~ subjects already taken.

void testStudentGpaCalculationReturnGradesAverageValue(void) {
    float expected = 2.5;
    int number_of_subjects = 6;
    struct Student student;
    student = initialize_student();
    
    struct Subject subjects[number_of_subjects]; 
    for (int i=0; i<number_of_subjects; i++){
        struct Subject subject = initialize_subject();
        subject.grade = i;
        subjects[i] = subject;
    }
    int length = sizeof(subjects) / sizeof(subjects[0]);
    
    student = calculate_student_gpa(student, subjects, length);

    TEST_ASSERT_EQUAL_FLOAT( expected, student.gpa );
}


void testStudentHasInitialGpaSetToZero(void) {
    struct Student student;
    student = initialize_student();
    
    TEST_ASSERT_EQUAL_FLOAT( 0, student.gpa );
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(testStudentGpaCalculationReturnGradesAverageValue);
    RUN_TEST(testStudentHasInitialGpaSetToZero);
    return UNITY_END();
}