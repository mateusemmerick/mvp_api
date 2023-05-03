from sqlalchemy import Column, ForeignKey, String, Integer
from model.base import Base

class EntradaProduto(Base):
    __tablename__ = 'entrada_produto'

    id = Column("pk_entrada", Integer, primary_key=True)        
    codigo = Column(String(10), ForeignKey("estoque_produto.pk_codigo"), nullable=False)
    quantidade = Column(Integer)
    data = Column(String(10))    
        

    def __init__(self, codigo:str, quantidade:int, data:str):    
        """
        Registra a entrada de um produto no estoque

        Argumentos:        
        código: código do produto
        quantidade: quantidade de produto adicionado ao estoque
        data: data de entrada
        """        
        self.codigo = codigo
        self.quantidade = quantidade
        self.data = data