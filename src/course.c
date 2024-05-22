#include "declarations.h"

struct Course initialize_course(char* name){
    struct Course course;
    course.name = name;
    // save to database and get the id
    course.id = 42;
    return course;  
}

struct University add_course(struct University university, struct Course course) {
    const int MIN_COURSES = 3;
    int lenght = university.num_courses;
    int *ptr2 = realloc(university.courses, lenght + sizeof(university.courses[0]));
    university.courses = ptr2;
    university.courses[lenght] = course.id;
    university.num_courses++;
    if (university.num_courses >= MIN_COURSES){
        university.active = 1;
    }
    return university;
}
