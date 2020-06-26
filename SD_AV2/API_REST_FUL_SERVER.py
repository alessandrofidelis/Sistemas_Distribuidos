import mysql.connector
from flask import Flask
import json
from flask_jsonpify import jsonify

app = Flask(__name__) # __name__ variável do sistema que indica o nome do módulo ou 'main'



#que recebe um parâmetro (nome do país) e retorna os clientes que residem naquele país;
@app.route("/lista_clientes/<pais>")
def lista_clientes(pais= None):
    conn = mysql.connector.connect (host='bd-sd2020-1.ceyopczt7djw.us-east-1.rds.amazonaws.com', user='admin', passwd='12345678', port='3306', database='chinook')
    cursor = conn.cursor()
    qstr = "select * from customers where country =\'"+pais+"\'"
    print (qstr)
    query = cursor.execute(qstr)
    row_headers=[x[0] for x in cursor.description]
    records = cursor.fetchall()
    print (records)
    result = [dict(zip(tuple (row_headers) ,i)) for i in records]
    #print (result)
    jret = jsonify(result)
    print (jret)
    conn.close()
    return jret

# que recebe um parâmetro (id do cliente) e retorna os ids dos pedidos (invoices) que o cliente fez;

@app.route("/lista_pedidos/<id_cliente>")
def lista_pedidos (id_cliente=None):
    conn = mysql.connector.connect (host='bd-sd2020-1.ceyopczt7djw.us-east-1.rds.amazonaws.com', user='admin', passwd='12345678', port='3306', database='chinook')
    cursor = conn.cursor()
    qstr = "select InvoiceId  from invoices where CustomerId ="+id_cliente
    print (qstr)
    query = cursor.execute(qstr)
    row_headers=[x[0] for x in cursor.description]
    records = cursor.fetchall()
    print (records)
    result = [dict(zip(tuple (row_headers) ,i)) for i in records]
    print (result)
    jret = jsonify(result)
    print (jret)
    conn.close()
    return jret
    
#que recebe um parâmetro (id do pedido) e retorna o valor total do pedido;
@app.route("/get_valor/<id_pedido>")
def get_valor (id_pedido=None):
    conn = mysql.connector.connect (host='bd-sd2020-1.ceyopczt7djw.us-east-1.rds.amazonaws.com', user='admin', passwd='12345678', port='3306', database='chinook')
    cursor = conn.cursor()
    qstr = "select total from invoices where InvoiceId ="+id_pedido
    print (qstr)
    query = cursor.execute(qstr)
    row_headers=[x[0] for x in cursor.description]
    records = cursor.fetchall()
    print (records)
    result = [dict(zip(tuple (row_headers) ,i)) for i in records]
    print (result)
    jret = jsonify(result)
    print (jret)
    conn.close()
    return jret
app.run(port='8080')
