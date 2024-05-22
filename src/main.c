#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "declarations.h"

const char* DATABASE = "university.db";

int are_text_equal(char text1[], char text2[]);
void show_help();

/* main.c */
int main(int argc, char *argv[]) {
    if ( ! argv[1] ){
        show_help();
        return 0;
    }

    if ( are_text_equal(argv[1], "init-database") )
    {
        if ( are_text_equal(argv[2], "test") ) {
            DATABASE = "test.db";
        }

        char* statement = "CREATE TABLE IF NOT EXISTS students"\
        " (id INTEGER PRIMARY KEY,name,state,cpf,gpa,subjects,course,semester_counter);";
        save_to_database(DATABASE, statement);

        statement = "CREATE TABLE IF NOT EXISTS courses"\
        " (id INTEGER PRIMARY KEY, name);";
        save_to_database(DATABASE, statement);
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
        char* statement = "INSERT INTO students VALUES ('name', 'state', 'cpf', 'identifier2', 3.4, 'subject', 'course', 1);";
        save_to_database(DATABASE, statement);

        printf("Student gpa is %f\n", student.gpa);
        return 0;
    }

    if ( are_text_equal(argv[1], "create-course") )
    {
        if (argc != 4){
            printf("Need to specify the name of the course.\n");
            return 1;
        }

        struct Course course = initialize_course();
        if ( are_text_equal(argv[2], "name") ) {
            course.name = argv[3];
        }

        struct University university = initialize_university();
        add_course(DATABASE, university, course);

        printf("Course '%s' created.\n", course.name);
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
        "create-course name *char"
        "init-database\n"
    );
}

int are_text_equal(char text1[], char text2[])
{
    return strcmp(text1, text2) == 0;
}