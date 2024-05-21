# https://makefiletutorial.com/
SRC_FILES := $(wildcard src/*.c)
EXCLUDE_FILES := $(wildcard src/*test*.c)
SRC_FILES := $(filter-out $(EXCLUDE_FILES), $(SRC_FILES))
TEST_FILES := src/student*.c src/subject*.c

compile:
	gcc $(SRC_FILES) -lpthread -ldl -o main.out

test:
	gcc $(TEST_FILES) ../unity/src/unity.c -o TestRunner; ./TestRunner