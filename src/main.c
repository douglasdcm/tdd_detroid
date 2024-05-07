#include <stdio.h>
#include "declarations.h"


/* main.c */
int main(int argc, char *argv[]) {
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
    printf("Result: %f\n", student.gpa);
}