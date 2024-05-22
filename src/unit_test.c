#include "../unity.h"
#include <string.h>
#include <stdlib.h>
#include "declarations.h"

void setUp(){}
void tearDown(){}

// COURSE
// 5. Initially, the university will have 3 courses with 3 subjects each.
void testInitializeUniversityWith3CourseAnd3SubjectsEach(void) {
    int expected = 1;
    struct University university;
    struct Course course1;
    struct Course course2;
    struct Course course3;

    university = initialize_university();
    course1 = initialize_course("course1");
    course2 = initialize_course("course2");
    course3 = initialize_course("course3");
    university = add_course(university, course1);
    university = add_course(university, course2);
    university = add_course(university, course3);

    TEST_ASSERT_EQUAL_INT( university.active, expected );
}

// STUDENT
// 1. Each student will have a grade control called "grade point average" (GPA).
// 2. The GPA is the average of the student's grades in the ~~courses~~ subjects already taken.
void testStudentCommandToSaveToDatabaseIsCorrect(void) {
    float expected = 2.5;
    int number_of_subjects = 6;
    struct Student student;
    student = initialize_student();
    student.name = "name";
    student.state = "state";
    student.cpf = "12345678910";
    student.gpa = 3.4;
    student.subject = "subject";
    student.course = "course";
    student.semester = 1;
    char statement[1000] = "";

    TEST_ASSERT_EQUAL_STRING( 
        "INSERT INTO students VALUES ('name','state','12345678910','any',3.4,'subject','course',1);"
        , build_statement_insert_student(student, statement) );
}

void testStudentGpaCalculationReturnGradesAverage(void) {
    float expected = 2.5;
    int number_of_subjects = 6;
    struct Student student;
    student = initialize_student();
    float gpa;
    struct Subject subjects[number_of_subjects]; 
    for (int i=0; i<number_of_subjects; i++){
        struct Subject subject = initialize_subject();
        subject.grade = i;
        subjects[i] = subject;
    }
    int length = sizeof(subjects) / sizeof(subjects[0]);
    
    gpa = calculate_student_gpa(student, subjects, length);

    TEST_ASSERT_EQUAL_FLOAT( expected, gpa );
}


void testStudentHasInitialGpaSetToZero(void) {
    struct Student student;
    student = initialize_student();
    
    TEST_ASSERT_EQUAL_FLOAT( 0, student.gpa );
}

int main(void)
{
    UNITY_BEGIN();
    //course
    RUN_TEST(testInitializeUniversityWith3CourseAnd3SubjectsEach);

    // student 
    RUN_TEST(testStudentGpaCalculationReturnGradesAverage);
    RUN_TEST(testStudentHasInitialGpaSetToZero);
    RUN_TEST(testStudentCommandToSaveToDatabaseIsCorrect);
    return UNITY_END();
}