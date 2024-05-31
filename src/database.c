#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


static int callback(void *NotUsed, int argc, char **argv, char **azColName){
    int i;
    for(i=0; i<argc; i++){
        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
    }
    printf("\n");
    return 0;
}

int run_on_database(char* database, char *statememt){
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    rc = sqlite3_open(database, &db);
    if( rc ){
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return(1);
    }
    rc = sqlite3_exec(db, statememt, callback, 0, &zErrMsg);
    if( rc!=SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    }
    sqlite3_close(db);
    return 0;
}

char** get_data_from_database(char* database, char* statement, char** result)
{
    sqlite3* db_ptr;
    sqlite3_stmt* stmt;
    char* errMesg = 0;
    // reference: https://stackoverflow.com/questions/12917727/resizing-an-array-in-c
    result = malloc(0); // array of chars, samoe of char* result[0], but is dinamically allocated
    char** ptr2 = malloc(0);

    int ret = 0;

    ret = sqlite3_open(database, &db_ptr);

    if (ret != SQLITE_OK) {
        printf("Database opening error\n");
    }

    char* sql_stmt = statement;

    ret = sqlite3_prepare_v2(db_ptr, sql_stmt, -1, &stmt, 0);

    if (ret != SQLITE_OK) {
        printf("\nUnable to fetch data");
        sqlite3_close(db_ptr);
        return result;
    }

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        int lenght = 0;
        // sqlite3_column_count() is used to know the number of columns
        // sqlite3_column_bytes() used to return the lenght of the column in bytes
        // reference: https://www.sqlite.org/c3ref/column_blob.html
        for (int i = 0; i < sqlite3_column_count(stmt); i++){
            lenght += sqlite3_column_bytes(stmt, i);
            ptr2 = realloc(result, lenght);
            result = ptr2;
            ptr2[i] = malloc(sqlite3_column_bytes(stmt, i));
            result[i] = ptr2[i];
            memcpy(result[i], (char*)sqlite3_column_text(stmt, i), sqlite3_column_bytes(stmt, i));
            // printf("'%s'\n", result[i]);
        }
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db_ptr);

    return result;
}
