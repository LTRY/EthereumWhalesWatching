import pymysql


def commit(_conn, addr_tab):
    conn = _conn
    cur = conn.cursor()
    for addr in addr_tab:
        cur.execute("INSERT INTO addr (address) VALUES ('{}');".format(addr))
    conn.commit()
    cur.close()


def show(_conn):
    conn = _conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM addr;")
    rows = cur.fetchall()
    for row in rows:
        print(" ", row[0], row[1])
    conn.commit()
    cur.close()


def main():
    _conn = pymysql.connect("127.0.0.1", "root", "*****", "ETH_ADDR")
    commit(_conn, ["0x7727e5113d1d161373623e5f49fd568b4f543a9e"])
    show(_conn)
    _conn.close()


if __name__ == '__main__':
    main()
