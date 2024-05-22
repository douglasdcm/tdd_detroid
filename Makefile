# https://makefiletutorial.com/
SRC_FILES := $(wildcard src/*.c)
EXCLUDE_FILES := $(wildcard src/*test*.c)
SRC_FILES := $(filter-out $(EXCLUDE_FILES), $(SRC_FILES))
TEST_FILES := src/unit_test.c src/student.c src/subject.c src/course.c src/university.c src/database.c src/sqlite3.c

compile:
	gcc $(SRC_FILES) -lpthread -ldl -o main.out

test:
	gcc $(TEST_FILES) ../unity/src/unity.c -lpthread -ldl -o TestRunner; ./TestRunner