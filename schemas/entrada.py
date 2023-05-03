import sys
sys.path.append('meu_app_api\model')
from pydantic import BaseModel
from typing import Optional, List
from model.entrada import EntradaProduto



class EntradaSchema(BaseModel):
    """ Define como uma nova entrada a ser inserida deve ser representada
    """
    codigo: str = "FB200"    
    quantidade: int = 10    
    id: int = 1
    data: str = "07/02/2023"  

class EntradaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita apenas com base no id da entrada.
    """
    id: int = 1


class ListagemEntradaSchema(BaseModel):
    """ Define como uma listagem de entradas será retornada.
    """
    entradas:List[EntradaSchema]


def apresenta_entradas(entradas: List[EntradaSchema]):
    """ Retorna uma representação das entradas seguindo o schema definido em
        EntradaSchema.
    """
    result = []
    for entrada in entradas:
        result.append({
            "codigo": entrada.codigo,            
            "quantidade": entrada.quantidade,
            "id": entrada.id,
            "data": entrada.data
        })

    return {"entradas": result}


class EntradaViewSchema(BaseModel):
    """ Define como uma entrada de um produto será retornado
    """
    codigo: str = "FB200"    
    quantidade: int = 10
    id: int = 1
    data: str = "07/02/2023" 


class EntradaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

def apresenta_entrada(entrada: EntradaProduto):
    """ Retorna uma representação da entrada do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "codigo": entrada.codigo,        
        "quantidade": entrada.quantidade,
        "id": entrada.id,
        "data": entrada.data
    }
