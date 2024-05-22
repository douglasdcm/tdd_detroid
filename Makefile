# https://makefiletutorial.com/
SRC_FILES := $(wildcard src/*.c)
EXCLUDE_FILES := $(wildcard src/*test*.c)
SRC_FILES := $(filter-out $(EXCLUDE_FILES), $(SRC_FILES))

TEST_FILES := $(wildcard src/*.c)
EXCLUDE_FROM_TEST := $(wildcard src/main.c)
TEST_FILES := $(filter-out $(EXCLUDE_FROM_TEST), $(TEST_FILES))

compile:
	gcc $(SRC_FILES) -lpthread -ldl -o main.out

test:
	gcc $(TEST_FILES) ../unity/src/unity.c -lpthread -ldl -o TestRunner; ./TestRunner