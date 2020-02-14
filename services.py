import sqlite3


def getPk(db, tab):
    cursor = db.cursor()
    cursor.execute("pragma table_info ('" + tab + "') ")
    data = cursor.fetchall()
    ind1 = []
    for i in data:
        if i[5] == 1:
            return i


def checkandcorrect(db, st, tab):
    cursor = db.cursor()
    cursor.execute("pragma table_info ('" + tab + "') ")
    data = cursor.fetchall()
    ok = True
    while ok:
        ok = False
        for i in data:
            if i[1] == st:
                ok = True
                st += '1'
                break
    return st


def myinit(db):
    st = """create table userTables (
                id integer primary key autoincrement, 
                tab text not null, 
                user text not null 
                )"""
    cursor = db.cursor()
    cursor.execute(st)
    db.commit()


def getTableDump(db_file, tables):
    conn = sqlite3.connect(':memory:')
    cu = conn.cursor()
    cu.execute("attach database '" + db_file + "' as attached_db")
    for table_to_dump in tables:
        cu.execute("select sql from attached_db.sqlite_master "
                   "where type='table' and name='" + table_to_dump + "'")
        sql_create_table = cu.fetchone()[0]
        cu.execute(sql_create_table);
        cu.execute("insert into " + table_to_dump +
                   " select * from attached_db." + table_to_dump)
    conn.commit()
    cu.execute("detach database attached_db")
    return conn.iterdump()


def getPort():
    from socket import socket, gethostbyname, AF_INET, SOCK_STREAM
    import random
    target = "localhost"
    targetIP = gethostbyname(target)
    s = socket(AF_INET, SOCK_STREAM)  # Инициализируем TCP-сокет
    while True:
        rid = random.randint(1000, 6500)  # Случайный порт
        result = s.connect_ex((targetIP, rid))
        if result != 0:
            s.close()
            return rid


def gettype(val):
    if val.isdigit():
        return "integer"
    elif val.replace('.', '', 1).isdigit():
        return "double"
    else:
        return "text"
