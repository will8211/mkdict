#!/usr/bin/env python3

import MySQLdb
import random
from romanization import *
from moe_dict import moe_dict

print('Moving on to the MOE dictionary...')

# Connect to database in SQL

conn = MySQLdb.connect(host="localhost", user='root', passwd='iamafish', 
                       db='mkdictionary', charset='utf8mb4')
cursor = conn.cursor()
SQL = cursor.execute

# (Re)create table 

SQL("DROP TABLE IF EXISTS Moe_dict")
SQL("""
    CREATE TABLE Moe_dict (
    Id          INT          UNSIGNED NOT NULL AUTO_INCREMENT,
    Type        BOOLEAN      NOT NULL,
    Chinese     VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    English     VARCHAR(512) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    POJ         VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    TRS         VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    DT          VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    POJ_search  VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    TRS_search  VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    DT_search   VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    POJ_numbers VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    TRS_numbers VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    DT_numbers  VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    Code        CHAR(4)      NOT NULL,
    Tai_char    VARCHAR(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
    PRIMARY KEY (id))
    """) # ENGINE=MyISAM (at the very end)

SQL("ALTER TABLE Moe_dict AUTO_INCREMENT = 2")

# Populate MySQL database

base64 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
used_codes = []

moe = moe_dict()

for i in range(len(moe)):
    if i % 2000 == 0:
        print('Writing row %d to mySQL table' % i)
    r = moe[i]
    boolean = int(r[1].startswith('::'))
    
    #Escape single-quotes
    r[3] = r[3].replace("'", "''")
    #Amend Taiwanese
    r[1] = r[1].replace('::', '')
    r[1] = r[1].replace('::', '')
    r[1] = r[1].replace('9', '2')
    #Chinese punctiation police!
    r[2] = r[2].replace(' ,', '，')
    r[2] = r[2].replace(' (', '（')
    r[2] = r[2].replace(' )', '）')
    r[2] = r[2].replace('!', '！')
    r[2] = r[2].replace('?', '？')
    
    poj, poj_search, poj_numbers = poj_convert(r[1])
    trs, trs_search, trs_numbers = trs_convert(r[1])
    dt, dt_search, dt_numbers = dt_convert(r[1])
    
    looking = True
    while looking:
        code = ''.join(random.choice(base64) for n in range(3))
        if code not in used_codes:
            looking = False
    used_codes.append(code)

    tai_char = r[4]
    if tai_char == '':
        tai_char = None

    SQL("""
        INSERT INTO Moe_dict (Type, Chinese, English, POJ, TRS, DT, 
                        POJ_search, TRS_search, DT_search,
                        POJ_numbers, TRS_numbers, DT_numbers, Code, Tai_char)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (boolean, r[2], r[3], poj, trs, dt, 
              poj_search, trs_search, dt_search, 
              poj_numbers, trs_numbers, dt_numbers, code, tai_char))

# Add sphinxsearch access table

d = 'Moe_dict'

SQL("DROP TABLE IF EXISTS %s_sphinx" % d)
SQL("""
    CREATE TABLE %s_sphinx (
    id          BIGINT UNSIGNED NOT NULL,
    weight      INTEGER NOT NULL,
    query       VARCHAR(256) NOT NULL,
    group_id    INTEGER,
    INDEX(query)
    ) ENGINE=SPHINX CONNECTION="sphinx://127.0.0.1:9312/%s";
    """ % (d, d))


#Fix for error "Illegal mix of collations (latin1_swedish_ci,IMPLICIT) and 
#(utf8_general_ci,COERCIBLE) for operation '='" as per 
#<stackoverflow.com/questions/1008287/illegal-mix-of-collations-mysql-error>

SQL("SET collation_connection = 'utf8_general_ci'")
SQL("ALTER DATABASE mkdictionary CHARACTER SET utf8 COLLATE utf8_general_ci")
SQL("ALTER TABLE Dict CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci")
SQL("ALTER TABLE Moe_dict CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci")
SQL("ALTER TABLE Dict_sphinx CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci")
SQL("ALTER TABLE Moe_dict_sphinx CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci")

# Commit changes and close connection

conn.commit()
cursor.close()
conn.close()


