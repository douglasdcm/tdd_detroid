#include <stdlib.h>
#include "declarations.h"

struct University initialize_university(){
    struct University university;
    int num_courses = 0;
    university.active = 0;
    university.num_courses = num_courses;
    university.courses = malloc(num_courses);
    return university;
};