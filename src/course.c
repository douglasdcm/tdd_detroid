#include <string.h>
#include "declarations.h"

struct Course initialize_course(char* name){
    struct Course course;
    course.name = name;
    // save to database and get the id
    course.id = 42;
    course.num_subjects = 0;
    return course;  
}

struct University add_course(const char* database, struct University university, struct Course course) {
    const int MIN_COURSES = 3;
    const int MIN_SUBJECTS = 3;
    int lenght = university.num_courses;
    int *ptr2 = realloc(university.courses, lenght + sizeof(university.courses[0]));
    university.courses = ptr2;
    university.courses[lenght] = course.id;
    university.num_courses++;

    char *tokens[] = {"INSERT INTO courses VALUES (NULL,'", course.name ,"',NULL);"};
    char statement[100] = "";
    for (int i = 0; i < 3; i++){ // 3 is the number of tokens
        strcat(statement, tokens[i]);
    }
    run_on_database(database, statement);
    
    if (university.num_courses >= MIN_COURSES){
        // get courses from database
        struct Course c1 = initialize_course("c1");
        struct Course c2 = initialize_course("c2");
        struct Course c3 = initialize_course("c3");
        struct Course courses[] = {c1,c2,c3};
        int lenght = sizeof(courses) / sizeof(courses[0]);
        for (int i = 0; i < lenght; i++){
            if (courses[i].num_subjects < MIN_SUBJECTS){
                break;
            }
        }
        university.active = 1;
    }
    return university;
}
