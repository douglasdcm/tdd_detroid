#include <stdio.h>
#include <sqlite3.h>
#include <stdlib.h>
#include <string.h>
#include "declarations.h"

const char* DATABASE = "university.db";

int are_text_equal(char text1[], char text2[]);
void show_help();
int save_to_database(const char* database, char *statememt);


/* main.c */
int main(int argc, char *argv[]) {
    if ( ! argv[1] ){
        show_help();
        return 0;
    }

    if ( are_text_equal(argv[1], "init-database") )
    {
        char* statement = "CREATE TABLE IF NOT EXISTS students"\
        " (name,state,cpf,identifier PRIMARY KEY,gpa,subjects,course,semester_counter);";
        return save_to_database(DATABASE, statement);
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


static int callback(void *NotUsed, int argc, char **argv, char **azColName){
    int i;
    for(i=0; i<argc; i++){
        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
    }
    printf("\n");
    return 0;
}

int save_to_database(const char* database, char *statememt){
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    rc = sqlite3_open(database, &db);
    if( rc ){
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return(1);
    }
    rc = sqlite3_exec(db, statememt, callback, 0, &zErrMsg);
    if( rc!=SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    }
    sqlite3_close(db);
    return 0;
}

void show_help()
{
    printf(
        "\n"
        "help\n"
        "create-student [gpa int]\n"
        "create-subject [grade int]\n"
        "init-database\n"
    );
}

int are_text_equal(char text1[], char text2[])
{
    return strcmp(text1, text2) == 0;
}