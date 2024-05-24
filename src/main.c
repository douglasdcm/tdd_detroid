#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "declarations.h"

extern const char* DATABASE;

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
        if (argc != 3){
            printf("Specify the type of database: test or prod\n");
            return 1;
        }
        int result = 0;

        if ( are_text_equal(argv[2], "test") ) {
            DATABASE = "test.db";
        }

        char* create_students = "CREATE TABLE IF NOT EXISTS students"\
        " (id INTEGER PRIMARY KEY,name VARCHAR(30) NOT NULL,state,cpf,gpa,subjects,course,semester_counter);";
        result = run_on_database(DATABASE, create_students);

        char* create_subjects = "CREATE TABLE IF NOT EXISTS subjects"\
        " (id INTEGER PRIMARY KEY, name VARCHAR(30) NOT NULL);";
        result = run_on_database(DATABASE, create_subjects);
        
        char* create_courses = "CREATE TABLE IF NOT EXISTS courses"\
        " (id INTEGER PRIMARY KEY, name VARCHAR(30) NOT NULL,"\
        " subject INTEGER, FOREIGN KEY(subject) REFERENCES subjects(id) );";
        result = run_on_database(DATABASE, create_courses);
        
        return result;
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
        char* statement = "INSERT INTO students VALUES ('name', 'state', 'cpf', NULL, 3.4, 'subject', 'course', 1);";
        run_on_database(DATABASE, statement);

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