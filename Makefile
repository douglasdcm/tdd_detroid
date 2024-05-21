# https://makefiletutorial.com/
SRC_FILES := $(wildcard src/*.c)
EXCLUDE_FILES := $(wildcard src/*test*.c)
SRC_FILES := $(filter-out $(EXCLUDE_FILES), $(SRC_FILES))

compile:
	gcc $(SRC_FILES) -lpthread -ldl -o main.out