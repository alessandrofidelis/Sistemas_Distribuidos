from socket import *
from threading import Thread, Condition,Lock
	
estoque = 1000
cond = Condition()
mutex = Lock()

def check(): 
	global estoque

	if (estoque < 100): 
		estoque += 1000
		return 1
	return 1


def atende (conn, cliente):
	global estoque
	pedido = 0
	conn.settimeout(30.00)
	while True:

		try:
			data = conn.recv (4096)
		except:
			print ("Erro na conexão com o cliente "+str(cliente))
			break
		if not data or len(data) == 0:
        		break
        	
		if data == b'':
			continue
		
		msgstr = str(data.decode("utf-8")).split()
		cont = int(msgstr[0])
		msg = int(msgstr[1])
	
		with cond:
			cond.wait_for (check)
			estoque -= msg
			print('Consumidor ' +str(cont)+ ' está solicitando '+str(msg)+' produtos')
			cond.notify_all()
	
	print ("Fim da conexao com "+str(cliente))
	conn.close()



s = socket ()
host = "0.0.0.0"
porta = 8792
s.bind ((host, porta))
s.listen (100)
nthr = 0

while True:
    (conn, cliente) = s.accept ()
    print ("Recebi a conexao de "+str(cliente))
    nthr += 1
    print ("Criando thread "+str(nthr))
    t = Thread(target=atende,args=(conn,cliente))
    t.start()