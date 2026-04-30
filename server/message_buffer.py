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
                    novo_nome = p['nome']
                    with self.mutex:
                        if novo_nome in self.clientes:
                            conn.sendall(json.dumps({'acao': 'erro', 'msg': 'Nome já em uso.'}).encode('utf-8'))
                        else:
                            nome = novo_nome
                            self.clientes[nome] = conn
                            
                elif p['acao'] == 'entrar_canal':
                    canal = p['canal']
                    with self.mutex:
                        if canal not in self.canais:
                            self.canais[canal] = []
                        if nome not in self.canais[canal]:
                            self.canais[canal].append(nome)
                
                elif p['acao'] == 'enviar':
                    with self.mutex:
                        alvos = []
                        if p['tipo'] == 'unicast':
                            if p['dest'] not in self.clientes:
                                conn.sendall(json.dumps({'acao': 'erro', 'msg': f'Usuário {p["dest"]} não encontrado ou offline.'}).encode('utf-8'))
                            else:
                                alvos = [self.clientes.get(p['dest'])]
                        elif p['tipo'] == 'multicast':
                            alvos = [self.clientes[c] for c in self.canais.get(p['dest'], []) if c in self.clientes]
                        elif p['tipo'] == 'broadcast':
                            alvos = list(self.clientes.values())
                        
                        for c in filter(None, alvos):
                            c.sendall(json.dumps(p).encode('utf-8'))

                elif p['acao'] == 'ack':
                    log = f"[T:{p['tp']}] {p['prod']} -> {nome} [T:{p['tc']}] | Conteúdo: {p['msg']}"
                    self.registrar_log(log)
        finally:
            if nome: 
                with self.mutex:
                    self.clientes.pop(nome, None)
                    for canal in self.canais.values():
                        if nome in canal:
                            canal.remove(nome)
            conn.close()

    def iniciar(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT)); s.listen()
        while True:
            c, a = s.accept()
            threading.Thread(target=self.tratar_cliente, args=(c, a)).start()

if __name__ == "__main__":
    MessageBus().iniciar()