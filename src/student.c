#include <stdio.h>
#include <string.h>
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

    sprintf(c, "%i", student.semester);
    strcat(statement, c);
    strcat(statement, ");");

    return statement;
}

