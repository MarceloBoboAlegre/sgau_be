from flask import Flask, render_template, redirect, request
import uteis as ut
import mysql.connector as delet

# CRUD
app = Flask(__name__)
app.config['SECRET_KEY'] = 'IpeRosa321'


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    senha = request.form.get('senha')
    con_senha = request.form.get('confirma_senha')
    if senha == con_senha:
        try:
            ut.cadastro_usuario(nome, email, telefone, senha)
        except Exception as erro:
            print(f'Houve um erro no cadastro! {erro.__class__}')
            return redirect('/')
        else:
            print("record inserted")
            return render_template('login.html')
    else:
        print('As senhas colocadas são diferentes')
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('usuario')
    senha = request.form.get('senha')
    logado = ut.login_usuario(nome, senha)
    if logado:
        return render_template('home.html')
    else:
        print('Senha ou Usuário incorretos!')
        return render_template('login.html')


@app.route('/cadastro.html')
def entrar_cadastro():
    return render_template('cadastro.html')


@app.route('/login')
def entrar_login():
    return render_template('login.html')


@app.route('/home.html')
def entrar_home():
    return render_template('home.html')


@app.route('/arvore_cadastro.html')
def entrar_arvore_cadastro():
    return render_template('arvore_cadastro.html')


@app.route('/arvore.html')
def entrar_arvores():
    return render_template('arvore.html')


@app.route('/configuracao.html')
def entrar_configuracao():
    return render_template('configuracao.html')


@app.route('/ocorrencia.html')
def entrar_ocorrencia():
    return render_template('ocorrencia.html')


@app.route('/relatorio.html')
def entrar_relatorio():
    return render_template('relatorio.html')


@app.route('/cadastro_arvore', methods=['POST'])
def cadastrar_arvore():
    ut.cadastro_arvore()


if __name__ in "__main__":
    app.run(debug=True)
