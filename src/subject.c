#include "declarations.h"

struct Subject initialize_subject(){
    struct Subject subject;
    subject.grade = 0;
    return subject;  
}

struct Course add_subject(char* database, struct Course course, struct Subject subject){
    course.num_subjects++;
    char* stm = "UPDATE courses SET subject = 1 WHERE id = 1;";
    run_on_database(database, stm);
    return course;
}
