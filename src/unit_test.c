#include "../unity.h"
#include <string.h>
#include "declarations.h"

char* TEST_DATABASE = "test.db";

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
    struct Subject subject1;
    struct Subject subject2;
    struct Subject subject3;

    university = initialize_university();
    course1 = initialize_course("course1");
    course2 = initialize_course("course2");
    course3 = initialize_course("course3");
    subject1 = initialize_subject();
    subject2 = initialize_subject();
    subject3 = initialize_subject();
    course1 = add_subject(TEST_DATABASE, course1, subject1);
    course1 = add_subject(TEST_DATABASE, course1, subject2);
    course1 = add_subject(TEST_DATABASE, course1, subject3);
    course2 = add_subject(TEST_DATABASE, course2, subject1);
    course2 = add_subject(TEST_DATABASE, course2, subject2);
    course2 = add_subject(TEST_DATABASE, course2, subject3);
    course3 = add_subject(TEST_DATABASE, course3, subject1);
    course3 = add_subject(TEST_DATABASE, course3, subject2);
    course3 = add_subject(TEST_DATABASE, course3, subject3);
    
    run_on_database(TEST_DATABASE, "select subject from courses where name = 'course1';");

    university = add_course(TEST_DATABASE, university, course1);
    university = add_course(TEST_DATABASE, university, course2);
    university = add_course(TEST_DATABASE, university, course3);

    TEST_ASSERT_EQUAL_INT( university.active, expected );
}


void testGetDataFromDatabase(void) {
    char** result;
    char** result2 = get_data_from_database(TEST_DATABASE, "SELECT * FROM courses;", result);
    
    printf("'%s'\n", result2[0]);

    TEST_ASSERT_EQUAL_INT( 0, 0 );
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
    RUN_TEST(testGetDataFromDatabase);
    return UNITY_END();
}