from flask import Flask, render_template, redirect, request, flash
import uteis as ut
import os

# APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'IpeRosa321'
logado = False

# ROTAS
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/cadastro.html')
def entrar_cadastro():
    return render_template('cadastro.html')


@app.route('/login')
def entrar_login():
    return render_template('login.html')


@app.route('/login.html')
def sair():
    global logado
    logado = False
    return redirect('/')


@app.route('/home.html')
def entrar_home():
    if logado:
        temp = ut.lista_arvores()
        quantia = len(temp)
        marcador = [quantia, temp]
        return render_template('home.html', marcador=marcador)
    else:
        flash('Não está logado!')
        return redirect('/')


@app.route('/arvore_cadastro.html')
def entrar_arvore_cadastro():
    if logado:
        return render_template('arvore_cadastro.html')
    else:
        flash('Não está logado!')
        return redirect('/')


@app.route('/arvore.html')
def entrar_arvores():
    if logado:
        tabela = ut.lista_arvores()
        return render_template('arvore.html', tabela=tabela)
    else:
        flash('Não está logado!')
        return redirect('/')


@app.route('/configuracao.html')
def entrar_configuracao():
    if logado:
        return render_template('configuracao.html')
    else:
        flash('Não está logado!')
        return redirect('/')


@app.route('/ocorrencia.html')
def entrar_ocorrencia():
    if logado:
        return render_template('ocorrencia.html')
    else:
        flash('Não está logado!')
        return redirect('/')


@app.route('/relatorio.html')
def entrar_relatorio():
    if logado:
        return render_template('relatorio.html')
    else:
        flash('Não está logado!')
        return redirect('/')


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    senha = request.form.get('senha')
    con_senha = request.form.get('confirma_senha')
    if senha == con_senha:
        try:
            res = ut.cadastro_usuario(nome, email, telefone, senha)
        except Exception as erro:
            print(f'Houve um erro no cadastro! {erro.__class__}')
            return redirect('/cadastro.html')
        else:
            if res:
                flash("Usuário Cadastrado com Sucesso!")
                return render_template('login.html')
            else:
                flash('Alguma informação já foi cadastrada!')
                return redirect('/cadastro.html')
    else:
        flash('As senhas colocadas são diferentes')
        return redirect('/cadastro.html')


@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('usuario')
    senha = request.form.get('senha')
    global logado
    logado = ut.login_usuario(nome, senha)
    if logado:
        return redirect('/home.html')
    else:
        flash('Senha ou Usuário incorretos!')
        return redirect('/')


@app.route('/cadastro_arvore', methods=['POST'])
def cadastrar_arvore():
    temp = ''
    arvore = {}
    lista = ['nome', 'especie', 'latitude', 'longitude', 'diametro_copa', 'altura_media', 'largura_calcada', 'pavimento',
             'largura_via_publica', 'fluxo_veiculos', 'passagem_pedestres', 'fluxo_pedestres', 'rede_eletrica',
             'elementos_proximos', 'tipo_sistema_radicular', 'afloramento', 'danos_passeio', 'projecao_raizes',
             'condicao_fitossanitaria', 'cavidade', 'termitas', 'coleobrocas', 'lesao', 'declinio', 'micelios',
             'anelamento', 'necrose', 'formigas', 'fungos', 'local_afetado', 'compromete_condicao_arvore', 'monitorar',
             'observacoes', 'data_cadastro']
    for k in lista:
        try:
            temp = request.form.get(k)
        except Exception as erro:
            print(f'Houve um erro no cadastro! {erro.__class__}')
            temp = ''
        finally:
            arvore[f"{k}"] = temp
    ut.cadastro_arvore(arvore)
    return render_template('relatorio.html')


@app.route('/pesquisa', methods=['POST'])
def pesquisar_arvore():
    codigo = request.form.get('codigo')
    nome_pop = request.form.get('nome_pop')
    data_cad = request.form.get('data_cadastro')
    res = {"id": '', "nome": '', "data_cadastro": ''}
    if codigo != '':
        res['id'] = codigo
    if nome_pop != '':
        res['nome'] = nome_pop
    if data_cad != '':
        res['data_cadastro'] = data_cad
    arvore_achada = ut.procurar_arvore(res)
    pesquisa = {'id': 0, 'cod_ref': 0, 'nome': '', 'especie': '', 'latitude': 0, 'longitude': 0, 
                'diametro_copa': 0, 'altura_media': 0, 'largura_calcada': 0, 'pavimento': '', 'largura_via_publica': '', 'fluxo_veiculos': 0, 'passagem_pedestres': '', 'fluxo_pedestres': 0, 'rede_eletrica': '', 'elementos_proximos': '', 'tipo_sistema_radicular': '', 'afloramento': '', 'danos_passeio': '', 'projecao_raizes': '','condicao_fitossanitaria': '', 'cavidade': '', 'termitas': '', 'coleobrocas': '', 'lesao': '', 'declinio': '', 'micelios': '', 'anelamento': '', 'necrose': '', 'formigas': '', 'fungos': '', 'local_afetado': '', 'compromete_condicao_arvore': '', 'monitorar': '', 'observacoes': '', 'data_cadastro': ''}
    c = 0
    for k in pesquisa.keys():
        if arvore_achada[c] == None:
            pesquisa[k] = 'Não possui'
        elif c > 16 and c != 35:
            if arvore_achada[c] == 1:
                pesquisa[k] = 'Possui'
            else:
                pesquisa[k] = 'Não possui'
        else:
            pesquisa[k] = arvore_achada[c]
        c += 1
    return render_template('pesquisa.html', pesquisa=pesquisa)


@app.route('/info')
def get_info():
    return render_template('info.html')


@app.route('/pesquisa.html')
def entrar_pesquisa():
    if logado:
        return render_template('pesquisa.html')
    else:
        flash('Não está logado!')
        return redirect('/')
