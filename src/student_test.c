#include "declarations.h"
#include "../unity.h"

#include <string.h>
#include <stdio.h>

void setUp(){}
void tearDown(){}

char* build_statement_insert_student(struct Student student, char* statement);

char* build_statement_insert_student(struct Student student, char* statement){
    strcpy(statement, "INSERT INTO students VALUES (");
    strcat(statement, "'");
    strcat(statement, student.name);
    strcat(statement, "',");
    
    strcat(statement, "'");
    strcat(statement, student.state);
    strcat(statement, "',");

    strcat(statement, "'");
    strcat(statement, student.cpf);
    strcat(statement, "',");

    strcat(statement, "'any',");

    char c[50];
    sprintf(c, "%g", student.gpa);
    strcat(statement, c);

    strcat(statement, ",'");
    strcat(statement, student.subject);
    strcat(statement, "',");

    strcat(statement, "'");
    strcat(statement, student.course);
    strcat(statement, "',");

    char snum[5];
    sprintf(c, "%i", student.semester);
    strcat(statement, c);
    strcat(statement, ");");

    return statement;
}

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

    strcpy(statement, build_statement_insert_student(student, statement));

    TEST_ASSERT_EQUAL_STRING( 
        "INSERT INTO students VALUES ('name','state','12345678910','any',3.4,'subject','course',1);"
        , statement );
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
    RUN_TEST(testStudentGpaCalculationReturnGradesAverage);
    RUN_TEST(testStudentHasInitialGpaSetToZero);
    RUN_TEST(testStudentCommandToSaveToDatabaseIsCorrect);
    return UNITY_END();
}