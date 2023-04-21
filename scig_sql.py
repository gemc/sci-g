#!/usr/bin/env python3

# Purposes:
# 1. function to create a sqlite database file with the geometry and materials tables
# 2. functions to fill the tables with the geometry and materials of a system

import argparse
import sys

NGIVEN: str = 'NOTGIVEN'
NGIVENS: [str] = ['NOTGIVEN']


def main():
    # Provides the -h, --help message
    desc_str = "   SCI-G sql interface\n"
    parser = argparse.ArgumentParser(description=desc_str)

    # file writers
    parser.add_argument('-l', metavar='<database name>', action='store', type=str,
                        help='creates an sqlite database file with geometry and materials tables', default=NGIVEN)

    args = parser.parse_args()

    if args.l != NGIVEN:
        create_sqlite_database(args.l)

    # if no argument is given print help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        print()
        sys.exit(1)


# create the database file (overwrite if it exists)
# create the tables geometry, materials, mirrors, parameters
def create_sqlite_database(sqlitedb):


    sql = sqlitedb.cursor()

    # Create table
    sql.execute('''CREATE TABLE geometry
                 (id integer primary key)''')

    # Save (commit) the changes
    sqlitedb.commit()


def add_fields_to_sqlite_if_needed(gvolume, configuration):

    sql = configuration.sqlitedb.cursor()

    # check if the table has the any field
    sql.execute("SELECT name FROM PRAGMA_TABLE_INFO('geometry');")
    fields = sql.fetchall()
    if len(fields) == 1:
        add_column(configuration.sqlitedb, "geometry", "system",    "TEXT")
        add_column(configuration.sqlitedb, "geometry", "variation", "TEXT")
        add_column(configuration.sqlitedb, "geometry", "run",       "INTEGER")
        # add columns from gvolume class
        for field in gvolume.__dict__:
            sql_type = sqltype_of_variable(gvolume.__dict__[field])
            add_column(configuration.sqlitedb, "geometry", field, sql_type)
    configuration.sqlitedb.commit()


def populate_sqlite_geometry(gvolume, configuration):
    add_fields_to_sqlite_if_needed(gvolume, configuration)

    sql = configuration.sqlitedb.cursor()

    # form a string representing the columns of the table
    columns = form_string_with_column_definitions(gvolume)
    values = form_string_with_column_values(gvolume, configuration)
    #print(columns)
    #print(values)
    sql.execute("INSERT INTO geometry {} VALUES {}".format(columns, values))
    configuration.sqlitedb.commit()


def form_string_with_column_definitions(gvolume) -> str:
    strn = "( system, variation, run, "
    for field in gvolume.__dict__:
        strn += f"{field}, "
    strn  = strn[:-2] + ")"
    return strn


def form_string_with_column_values(gvolume, configuration) -> str:
    strn = "( '{}', '{}', {}, ".format(configuration.system, configuration.variation, configuration.runno)
    for field in gvolume.__dict__:
        value = gvolume.__dict__[field]
        if type(value) is str:
            value = "'{}'".format(value)
        strn += f"{value}, "
    strn  = strn[:-2] + ")"
    return strn


def sqltype_of_variable(variable) -> str:
    if type(variable) is int:
        return 'INT'
    elif type(variable) is str:
        return 'TEXT'

def add_column(db, tablename, column_name, var_type):
    sql = db.cursor()
    strn = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(tablename, column_name, var_type)
    # print(strn)
    sql.execute(strn)
    db.commit()


if __name__ == "__main__":
    main()
