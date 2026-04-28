import socket
import threading
import json
import os

HOST = '127.0.0.1'
PORT = 5000

class MessageBus:
    def __init__(self):
        self.clientes = {}
        self.canais = {}
        self.mutex = threading.Lock()
        os.makedirs('server', exist_ok=True)

    def registrar_log(self, log):
        with self.mutex:
            with open('server/auditoria_log.txt', 'a', encoding='utf-8') as f:
                f.write(f"{log}\n")

    def tratar_cliente(self, conn, addr):
        nome = None
        try:
            while True:
                dados = conn.recv(4096)
                if not dados: break
                p = json.loads(dados.decode('utf-8'))
                
                if p['acao'] == 'registrar':
                    nome = p['nome']
                    with self.mutex: self.clientes[nome] = conn
                
                elif p['acao'] == 'enviar':
                    with self.mutex:
                        alvos = []
                        if p['tipo'] == 'unicast': alvos = [self.clientes.get(p['dest'])]
                        elif p['tipo'] == 'multicast': alvos = [self.clientes[c] for c in self.canais.get(p['dest'], [])]
                        
                        for c in filter(None, alvos):
                            c.sendall(json.dumps(p).encode('utf-8'))

                elif p['acao'] == 'ack':
                    log = f"[T:{p['tp']}] {p['prod']} -> {nome} [T:{p['tc']}] | Conteúdo: {p['msg']}"
                    self.registrar_log(log)
        finally:
            if nome: 
                with self.mutex: self.clientes.pop(nome, None)
            conn.close()

    def iniciar(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT)); s.listen()
        while True:
            c, a = s.accept()
            threading.Thread(target=self.tratar_cliente, args=(c, a)).start()

if __name__ == "__main__":
    MessageBus().iniciar()