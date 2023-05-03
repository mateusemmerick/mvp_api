from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from typing import Union


from model.base import Base

class EstoqueProduto(Base):
    __tablename__ = 'estoque_produto'
    
    codigo = Column('pk_codigo', String(10), primary_key=True)
    nome = Column(String(200))    
    quantidade = Column(Integer)
    valor = Column(Float)    

    def __init__(self, nome:str, codigo:str, quantidade:int, valor:float):
        """
        Registra um produto no estoque

        Argumentos:
        código: código do produto (primary key)
        nome: nome do produto        
        quantidade: quantidade de produto no estoque
        valor: valor de venda do produto        
        """
        self.nome = nome
        self.codigo = codigo
        self.quantidade = quantidade
        self.valor = valor