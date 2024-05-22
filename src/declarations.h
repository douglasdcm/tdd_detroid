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
    char* name;
    int id;
};

int save_to_database(const char* database, char *statememt);
struct Student initialize_student();
struct Subject initialize_subject();
struct Course initialize_course();
struct University initialize_university();
float calculate_student_gpa(
    struct Student student, struct Subject subjects[], int length);
char* build_statement_insert_student(struct Student student, char* statement);
struct University add_course(const char* database, struct University university, struct Course course);