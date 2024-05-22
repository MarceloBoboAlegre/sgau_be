import flask
import mysql.connector


def conectar_bd(h, u, pw, db):
    database = mysql.connector.connect(
        host = h,
        user = u,
        password = pw,
        database = db
    )
    return database


def cursor_on(database):
    mycursor = database.cursor()
    return mycursor


def turnoff(cursor, database):
    cursor.close()
    database.close()


def cadastro_usuario(nome, email, telefone, senha):
    db = conectar_bd('localhost', 'root', 'Coisadenerd2431$', 'sgau')
    myc = cursor_on(db)
    sql = ('INSERT INTO user (NOME, PASSWORD_HASH, EMAIL, TELEFONE, STATUS, NIVEL_ACESSO) '
           'VALUES (%s, %s, %s, %s, %s, %s)')
    val = (nome, senha, email, telefone, 'ACTIVE', 'USUÁRIO')
    myc.execute(sql, val)
    db.commit()
    turnoff(myc, db)


def login_usuario(nome, senha):
    db = conectar_bd('localhost', 'root', 'Coisadenerd2431$', 'sgau')
    myc = cursor_on(db)
    sql = 'SELECT * FROM user WHERE NOME = %s'
    prc = (nome, )
    try:
        myc.execute(sql, prc)
        res = myc.fetchone()
    except Exception as erro:
        print(f'Usuário não encontrado! {erro.__class__}')
    else:
        if senha == res[2]:
            return True
        else:
            return False
    finally:
        turnoff(myc, db)
