import sys
sys.path.append('meu_app_api\model')
from pydantic import BaseModel
from typing import Optional, List
from model.saida import SaidaProduto


class SaidaSchema(BaseModel):
    """ Define como uma nova saida (venda) de um produto a ser registrada deve ser representada
    """
    codigo: str = "FB200"    
    quantidade: int = 2    
    data: str = "15/03/2023" 
    cliente: str = "Mateus"
    valor: float = 179.80    
    id: int = 1


class SaidaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no código do produto.
    """
    id: int = 1


class ListagemSaidaSchema(BaseModel):
    """ Define como uma listagem de saidas será retornada.
    """
    saidas:List[SaidaSchema]


def apresenta_saidas(saidas: List[SaidaSchema]):
    """ Retorna uma representação das saidas seguindo o schema definido em
        SaidaSchema.
    """
    result = []
    for saida in saidas:
        result.append({
            "codigo": saida.codigo,            
            "quantidade": saida.quantidade,
            "cliente": saida.cliente,
            "valor": saida.valor,            
            "data": saida.data,
            "id": saida.id
        })

    return {"saidas": result}


class SaidaViewSchema(BaseModel):
    """ Define como um produto será retornado
    """
    codigo: str = "FB200"    
    quantidade: int = 2
    cliente: str = "Mateus"
    valor: float = 179.80    
    data: str = "15/03/2023"
    id: int = 1


class SaidaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_saida(saida: SaidaProduto):
    """ Retorna uma representação da saida (venda) do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "codigo": saida.codigo,        
        "quantidade": saida.quantidade,
        "cliente": saida.cliente,
        "valor": saida.valor,        
        "data": saida.data,
        "id": saida.id
    }
