#include <stdio.h>
#include "declarations.h"

// https://www.geeksforgeeks.org/using-sizof-operator-with-array-paratmeters-in-c/
struct Student calculate_student_gpa(
    struct Student student, struct Subject subjects[], int length) {
    int gpa = 0;
    for (int i; i < length; i++){
        gpa += subjects[i].grade;
    }
    student.gpa = (float) gpa / length;
    return student;
}

struct Student initialize_student(){
    struct Student student;
    student.gpa = 0;
    return student;  
}

struct Subject initialize_subject(){
    struct Subject subject;
    subject.grade = 0;
    return subject;  
}