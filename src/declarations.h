struct Student {
    float gpa;
};

struct Subject {
    float grade;
};

struct Student initialize_student();
struct Subject initialize_subject();
struct Student calculate_student_gpa(
    struct Student student, struct Subject subjects[], int length);
