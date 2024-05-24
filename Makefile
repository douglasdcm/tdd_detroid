# https://makefiletutorial.com/
SRC_FILES := $(wildcard src/*.c)
EXCLUDE_FILES := $(wildcard src/*test*.c)
SRC_FILES := $(filter-out $(EXCLUDE_FILES), $(SRC_FILES))

TEST_FILES := $(wildcard src/*.c)
EXCLUDE_FROM_TEST := $(wildcard src/main.c)
TEST_FILES := $(filter-out $(EXCLUDE_FROM_TEST), $(TEST_FILES))

DATABASE_PROD := university.db
DATABASE_TEST := test.db
MAIN = main.out

compile:
	rm -f $(DATABASE_PROD)
	touch $(DATABASE_PROD)
	gcc $(SRC_FILES) -lpthread -ldl -o $(MAIN)
	./$(MAIN) init-database prod

test:
	rm -f $(DATABASE_TEST)
	touch $(DATABASE_TEST)
	./$(MAIN) init-database test
	gcc $(TEST_FILES) ../unity/src/unity.c -lpthread -ldl -o TestRunner; ./TestRunner
