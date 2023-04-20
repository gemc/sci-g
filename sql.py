#!/usr/bin/env python3

# Purposes:
# 1. function to create a sqlite database file with the geometry and materials tables
# 2. functions to fill the tables with the geometry and materials of a system

# imports: do not edit these lines
import argparse
import os

NGIVEN: str = 'NOTGIVEN'
NGIVENS: [str] = ['NOTGIVEN']

from db_map import GEOMETRY_MAP



def main():
    # Provides the -h, --help message
    desc_str = "   SCI-G sql interface\n"
    parser = argparse.ArgumentParser(description=desc_str)

    # file writers
    parser.add_argument('-l', metavar='<database name>', action='store', type=str,
                        help='creates an sqlite database file with geometry and materials tables', default=NGIVEN)

    args = parser.parse_args()

    # print(vars(args))

    if args.l != NGIVEN:
        create_sqlite_database(args.l)


# create the database file (overwrite if it exists)
# create the tables geometry, materials, mirrors, parameters
def create_sqlite_database(db_file):
    filename=db_file+".db"

    # remove file if it exists
    try:
        os.remove(filename)
        print("Removed existing database file: {}".format(filename))
    except OSError:
        pass

    print("Creating database file: {}".format(filename))

    import sqlite3
    # overwrite file if it exists
    db = sqlite3.connect(filename)
    sql = db.cursor()

    # Create table
    sql.execute('''CREATE TABLE geometry
                 (id integer primary key, name text, type text, x real, y real, z real, dx real, dy real, dz real, 
                 rx real, ry real, rz real, material text, mirror text, parameters text)''')

    # Save (commit) the changes
    db.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed, or they will be lost.
    db.close()


if __name__ == "__main__":
    main()
