import socket
import threading
import json
from utils.relogio_logico import RelogioLogico
from crypto.seguranca import MotorSeguranca

class ClienteBus:
    def __init__(self):
        self.relogio = RelogioLogico()
        self.seguranca = MotorSeguranca()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nome = ""

    def receber(self):
        while True:
            data = self.socket.recv(4096)
            p = json.loads(data.decode('utf-8'))
            self.relogio.sincronizar(p['tp'])
            msg = self.seguranca.desproteger(p['msg'])
            print(f"\n[Recebido de {p['prod']} | T:{p['tp']}]: {msg}")
            
            # Envia ACK para auditoria
            ack = {'acao': 'ack', 'prod': p['prod'], 'tp': p['tp'], 'tc': self.relogio.incrementar(), 'msg': p['msg']}
            self.socket.sendall(json.dumps(ack).encode('utf-8'))

    def conectar(self):
        self.socket.connect(('127.0.0.1', 5000))
        self.nome = input("Nome: ")
        self.socket.sendall(json.dumps({'acao': 'registrar', 'nome': self.nome}).encode('utf-8'))
        threading.Thread(target=self.receber, daemon=True).start()
        
        while True:
            dest = input("Para (ou 'sair'): ")
            if dest == 'sair': break
            txt = input("Mensagem: ")
            tp = self.relogio.incrementar()
            p = {'acao': 'enviar', 'tipo': 'unicast', 'dest': dest, 'prod': self.nome, 'tp': tp, 'msg': self.seguranca.proteger(txt)}
            self.socket.sendall(json.dumps(p).encode('utf-8'))

if __name__ == "__main__":
    ClienteBus().conectar()