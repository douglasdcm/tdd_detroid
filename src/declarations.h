#include <stdlib.h>

struct Student {
    float gpa;
    char* name;
    char* state;
    char* cpf;
    char* subject;
    char* course;
    int semester;
};

struct Subject {
    float grade;
};

struct University {
    int active; // 0 active, 1 inactive
    int* courses; // list of course ids
    int num_courses; // counter of courses
};

struct Course {
    int id;
    char* name;
    int num_subjects;
};

int run_on_database(const char* database, char *statememt);
char** get_data_from_database(char* database, char* statement, char** result);
struct Student initialize_student();
struct Subject initialize_subject();
struct Course initialize_course();
struct University initialize_university();
float calculate_student_gpa(
    struct Student student, struct Subject subjects[], int length);
char* build_statement_insert_student(struct Student student, char* statement);
struct University add_course(const char* database, struct University university, struct Course course);
struct Course add_subject(char* database, struct Course course, struct Subject subject);