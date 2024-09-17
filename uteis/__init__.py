import mysql.connector
import bcrypt


def conectar_bd(h, u, pw, db):
    database = mysql.connector.connect(
        host=h,
        user=u,
        password=pw,
        database=db
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
    igual = False
    sen = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(sen, salt)

    lista = [nome, email, telefone, hash_senha]
    cod = ['nome', 'email', 'telefone', 'password_hash']
    for c in range(0, 4):
        sql = f"SELECT * FROM user WHERE {cod[c]} ='{lista[c]}'"
        try:
            myc.execute(sql)
        except:
            print('ok')
        else:
            res = myc.fetchone()
            print(res)
        finally:
            if res != None:
                igual = True
                break
    if igual:
        return False
    else:
        sql = ('INSERT INTO user (NOME, PASSWORD_HASH, EMAIL, TELEFONE, STATUS, NIVEL_ACESSO) '
            'VALUES (%s, %s, %s, %s, %s, %s)')
        val = (nome, hash_senha, email, telefone, 'ACTIVE', 'USUÁRIO')
        myc.execute(sql, val)
        db.commit()
        turnoff(myc, db)
        return True


def login_usuario(nome, senha):
    db = conectar_bd('localhost', 'root', 'Coisadenerd2431$', 'sgau')
    myc = cursor_on(db)
    sql = 'SELECT * FROM user WHERE NOME = %s'
    prc = (nome, )
    sen = senha.encode('utf-8')
    try:
        myc.execute(sql, prc)
        res = myc.fetchone()
    except Exception as erro:
        print(f'Usuário não encontrado! {erro.__class__}')
    else:
        try: 
            if bcrypt.checkpw(sen, res[2].encode('utf-8')):
                return True
            else:
                return False
        except:
            return False
    finally:
        turnoff(myc, db)


def cadastro_arvore(arvore):
    db = conectar_bd('localhost', 'root', 'Coisadenerd2431$', 'sgau')
    myc = cursor_on(db)
    sql = 'INSERT INTO arvores ('
    val = []
    c = 0
    for k, v in arvore.items():
        if c == 0:
            sql += f'{k.capitalize()}'
        else:
            sql += f', {k.capitalize()}'
        if v == 'on':
            val.append(True)
        else:
            val.append(v)
        c += 1
    sql += (') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
            ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    myc.execute(sql, val)
    db.commit()
    turnoff(myc, db)


def procurar_arvore(resposta):
    db = conectar_bd('localhost', 'root', 'Coisadenerd2431$', 'sgau')
    myc = cursor_on(db)
    for k, v in resposta.items():
        sql = f"SELECT * FROM arvores WHERE {k.capitalize()} ='{v}'"
        try:
            myc.execute(sql)
        except Exception as erro:
            print(f'Não encontrado! {erro.__class__}')
        else:
            res = myc.fetchone()
            break
    turnoff(myc, db)
    return res


def lista_arvores():
    db = conectar_bd('localhost', 'root', 'Coisadenerd2431$', 'sgau')
    myc = cursor_on(db)
    sql = 'SELECT * FROM arvores'
    myc.execute(sql)
    res = myc.fetchall()
    lista = list()
    dicionario = dict()
    for a in res:
        dicionario['latitude'] = a[4]
        dicionario['longitude'] = a[5]
        dicionario['id'] = a[0]
        dicionario['nome'] = a[2]
        dicionario['especie'] = a[3]
        dicionario['data_cadastro'] = a[35]
        lista.append(dicionario.copy())
    turnoff(myc, db)
    return lista


def marcar_mapa():
    db = conectar_bd('localhost', 'root', 'Coisadenerd2431$', 'sgau')
    myc = cursor_on(db)
    sql = 'SELECT * FROM arvores'
    myc.execute(sql)
    res = myc.fetchall()
    lista = list()
    dicionario = dict()
    for a in res:
        dicionario['latitude'] = float(a[4])
        dicionario['longitude'] = float(a[5])
        lista.append(dicionario.copy())
    print(lista)
    turnoff(myc, db)
    return lista
