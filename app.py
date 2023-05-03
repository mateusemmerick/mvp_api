from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError


from model import Session, EstoqueProduto, EntradaProduto, SaidaProduto
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Documentação em Swagger")
estoque_produto_tag = Tag(name="Estoque Produto", description="Adição, visualização, edição e remoção de produtos a tabela de estoque")
entrada_produto_tag = Tag(name="Entrada Produto", description="Adição, visualização e remoção de produtos a tabela de entrada")
saida_produto_tag = Tag(name="Saida Produto", description="Adição, visualização e remoção de produtos a tabela de saida")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger, que é a documentação swagger.
    """
    return redirect('/openapi/swagger')


@app.get('/produtos', tags=[estoque_produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os produtos cadastrados no estoque.

    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(EstoqueProduto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200

@app.post('/produto', tags=[estoque_produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo produto ao estoque.

    Retorna uma representação dos produtos.
    """
    produto = EstoqueProduto(
        codigo=form.codigo,
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor)
    logger.debug(f"Adicionando produto de código: '{produto.codigo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto de código: '{produto.codigo}'")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do código é a provável razão do IntegrityError
        error_msg = "Produto de mesmo código já salvo na base:/"
        logger.warning(f"Erro ao adicionar produto '{produto.codigo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar o novo item:/"
        logger.warning(f"Erro ao adicionar produto '{produto.codigo}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.delete('/produto', tags=[estoque_produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um produto do estoque a partir do código informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    codigo_produto = query.codigo
    print(codigo_produto)
    logger.debug(f"Deletando dados sobre produto #{codigo_produto}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(EstoqueProduto).filter(EstoqueProduto.codigo == codigo_produto).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto de código {codigo_produto}")
        return {"mesage": "Produto removido", "código": codigo_produto}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base:/"
        logger.warning(f"Erro ao deletar produto código '{codigo_produto}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.put('/produto/<string:codigo>', tags=[estoque_produto_tag],
            responses={"200":ProdutoViewSchema, "404":ErrorSchema})
def merge_produto(path:ProdutoBuscaSchema, form:ProdutoSchema):
    """Edita um produto da base de dados.

    Retorna uma representação dos produtos.
    """
    produto = EstoqueProduto(
        codigo=form.codigo,
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor)
    logger.debug(f"Editando produto de código: '{produto.codigo}'")
    try:
        # criando conexão com a base
        session = Session()
        produtoUpdate = session.query(EstoqueProduto).get(path.codigo)
        produtoUpdate.codigo = produto.codigo
        produtoUpdate.nome = produto.nome
        produtoUpdate.quantidade = produto.quantidade
        produtoUpdate.valor = produto.valor        
        # atualizando produto        
        session.commit()
        logger.debug(f"Atualizado produto de código: '{produto.codigo}'")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do código é a provável razão do IntegrityError
        error_msg = "Produto de mesmo código já salvo na base:/"
        logger.warning(f"Erro ao adicionar produto '{produto.codigo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item:/"
        logger.warning(f"Erro ao adicionar produto '{produto.codigo}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/entradas', tags=[entrada_produto_tag],
         responses={"200": ListagemEntradaSchema, "404": ErrorSchema})
def get_entradas():
    """Faz a busca por todas as entradas cadastradas.

    Retorna uma representação da listagem de entradas.
    """
    logger.debug(f"Coletando entradas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    entradas = session.query(EntradaProduto).all()

    if not entradas:
        # se não há entradas cadastrados
        return {"entradas": []}, 200
    else:
        logger.debug(f"%d entradas econtradas" % len(entradas))
        # retorna a representação de entradas
        print(entradas)
        return apresenta_entradas(entradas), 200

@app.post('/entrada', tags=[entrada_produto_tag],
          responses={"200": EntradaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_entrada(form: EntradaSchema):
    """Adiciona uma nova entrada à base de dados.

    Retorna uma representação das entradas.
    """
    entrada = EntradaProduto(
        codigo=form.codigo,        
        quantidade=form.quantidade,
        data=form.data
        )
    logger.debug(f"Adicionando entrada de código: '{entrada.codigo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando entrada
        session.add(entrada)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado entrada de código: '{entrada.codigo}'")
        return apresenta_entrada(entrada), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar entrada '{entrada.codigo}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.delete('/entrada', tags=[entrada_produto_tag],
            responses={"200": EntradaDelSchema, "404": ErrorSchema})
def del_entrada(query: EntradaBuscaSchema):
    """Deleta uma entrada a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    id = query.id        
    logger.debug(f"Deletando entrada de Id #{id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(EntradaProduto).filter(EntradaProduto.id == id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto de Id #{id}")
        return {"mesage": "Produto removido", "id": id}
    else:
        # se o id não foi encontrado
        error_msg = "Id não encontrado na base :/"
        logger.warning(f"Erro ao deletar id #'{id}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.get('/saidas', tags=[saida_produto_tag],
         responses={"200": ListagemSaidaSchema, "404": ErrorSchema})
def get_saidas():
    """Faz a busca por todas as saidas cadastradas.

    Retorna uma representação da listagem de saidas.
    """
    logger.debug(f"Coletando saidas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    saidas = session.query(SaidaProduto).all()

    if not saidas:
        # se não há saidas cadastrados
        return {"saidas": []}, 200
    else:
        logger.debug(f"%d saidas econtradas" % len(saidas))
        # retorna a representação de saidas
        print(saidas)
        return apresenta_saidas(saidas), 200

@app.post('/saida', tags=[saida_produto_tag],
          responses={"200": SaidaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_saida(form: SaidaSchema):
    """Adiciona uma nova saida à base de dados.

    Retorna uma representação das saidas.
    """
    saida = SaidaProduto(
        codigo=form.codigo,        
        quantidade=form.quantidade,
        cliente=form.cliente,
        valor=form.valor,        
        data=form.data
        )
    logger.debug(f"Adicionando saida de código: '{saida.codigo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando saida
        session.add(saida)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado saida de código: '{saida.codigo}'")
        return apresenta_saida(saida), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar saida '{saida.codigo}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.delete('/saida', tags=[saida_produto_tag],
            responses={"200": SaidaDelSchema, "404": ErrorSchema})
def del_saida(query: SaidaBuscaSchema):
    """Deleta uma saida a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    id = query.id
    print(id)
    logger.debug(f"Deletando saida de Id #{id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(SaidaProduto).filter(SaidaProduto.id == id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto de Id #{id}")
        return {"mesage": "Produto removido", "id": id}
    else:
        # se o id não foi encontrado
        error_msg = "Id não encontrado na base :/"
        logger.warning(f"Erro ao deletar id #'{id}', {error_msg}")
        return {"mesage": error_msg}, 404
