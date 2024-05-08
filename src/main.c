#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "declarations.h"

int are_text_equal(char text1[], char text2[]);
void show_help();


/* main.c */
int main(int argc, char *argv[]) {
    if ( ! argv[1] ){
        show_help();
        return 0;
    }

    if ( are_text_equal(argv[1], "help") )
    {
        show_help();
        return 0;
    }

    if ( are_text_equal(argv[1], "create-student") )
    {
        struct Student student = initialize_student();
        for (int j=2; j<argc; j++) {
            if ( are_text_equal(argv[j], "gpa") ) {
                student.gpa = atof(argv[j + 1]);
            }
        }
        printf("Student gpa is %f\n", student.gpa);
        return 0;
    }

    if ( are_text_equal(argv[1], "create-subject") )
    {
        struct Subject subject = initialize_subject();
        for (int j=2; j<argc; j++) {
            if ( are_text_equal(argv[j], "grade") ) {
                subject.grade = atof(argv[j + 1]);
            }
        }
        printf("Subject grade is %f\n", subject.grade);
        return 0;
    }

    printf("Invalid command. Try 'help'\n");
}

void show_help()
{
    printf(
        "\n"
        "help\n"
        "create-student [gpa int]\n"
        "create-subject [grade int]\n"
    );
}

int are_text_equal(char text1[], char text2[])
{
    return strcmp(text1, text2) == 0;
}