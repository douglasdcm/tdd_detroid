#include <stdio.h>
#include "declarations.h"


// https://www.geeksforgeeks.org/using-sizof-operator-with-array-paratmeters-in-c/
float calculate_student_gpa(
    struct Student student, struct Subject subjects[], int length) {
    int gpa = 0;
    for (int i; i < length; i++){
        gpa += subjects[i].grade;
    }
    return (float) gpa / length;
}


struct Student initialize_student(){
    struct Student student;
    student.gpa = 0;
    return student;  
}
