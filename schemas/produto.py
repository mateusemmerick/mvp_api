import sys
sys.path.append('meu_app_api\model')
from pydantic import BaseModel
from typing import Optional, List
from model.produto import EstoqueProduto

class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido ao estoque deve ser representado
    """
    codigo: str = "FB200"
    nome: str = "Fresh Bamboo - 200"
    quantidade: int = 10
    valor: float = 89.90


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita apenas com base no código do produto.
    """
    codigo: str = "FB200"


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[EstoqueProduto]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "codigo": produto.codigo,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "valor": produto.valor,
        })

    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado
    """
    codigo: str = "FB200"
    nome: str = "Fresh Bamboo - 200"
    quantidade: int = 10
    valor: float = 89.90


class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_produto(produto: EstoqueProduto):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "codigo": produto.codigo,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "valor": produto.valor
    }
