from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship
from typing import Union


from model.base import Base

class SaidaProduto(Base):
    __tablename__ = 'saida_produto'

    id = Column("pk_entrada", Integer, primary_key=True)        
    codigo = Column(String(10), ForeignKey("estoque_produto.pk_codigo"), nullable=False)
    quantidade = Column(Integer)
    data = Column(String(10))
    cliente = Column(String(100))
    valor = Column(Float)    
    
    

    def __init__(self, codigo:str, quantidade:int, data:str, cliente:str , valor:float):
    # def __init__(self, codigo:str, quantidade:int, data:DateTime, cliente:str , valor:float):
        """
        Registra a saída (venda) de um produto do estoque

        Argumentos:        
        código: código do produto
        quantidade: quantidade do produto vendida
        data: data de entrada
        cliente: nome do cliente
        valor: valor de venda do produto        
        """        
        self.codigo = codigo
        self.quantidade = quantidade
        self.data = data
        self.cliente = cliente
        self.valor = valor        
