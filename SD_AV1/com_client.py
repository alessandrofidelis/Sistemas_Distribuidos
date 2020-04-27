from threading import Thread,Lock
from socket import *
import random
import time

mutex = Lock()
produto = []
porc = []
threads = []

s = socket ()
s.connect(("127.0.0.1", 8792))

consumidor = int(input("Digite o número de consumidores: "))
    
def total_prod(i):
    global produto 
    produto.append(random.randint(100,1000)) #solicita pedidos entre 100 e 1000
    print('Consumidor '+ str(i) +': Pedido total é de '+ str(produto[i]) +' produtos.')
    porc.append(produto[i]//10) 
    num_pedido = 11
    
    for j in range (num_pedido):
        mutex.acquire()
        time.sleep(random.randint(1,10))
        porcentagem = str.encode(str(i)+" "+str(porc[i]), "UTF-8") 
        s.sendall(porcentagem)
        print('Consumidor '+str(i)+': Pedido '+str(j)+' de '+str(porc[i])+' produtos realizado com sucesso.')
        mutex.release()
        time.sleep(random.randint(1,10))
    
    mutex.acquire()
    resto = produto[i]%10
    fim = str.encode(str(i)+" "+str(resto), "UTF-8")
    print('Consumidor '+str(i)+': Pedido '+str(11)+' de '+str(resto)+' produtos realizado com sucesso.')
    s.sendall(fim)
    print('Consumidor '+str(i)+': Todos os pedidos concluídos.')
    mutex.release()
    



for i in range(consumidor):
    print('Disparando consumidor '+str(i))
    
    threads.append(Thread(target=total_prod,args=(i,)))
    threads[-1].start()

for i in range (consumidor):
    print("Aguardando thread "+str(i))
    threads[i].join()

 
s.close ()