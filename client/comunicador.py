import socket
import threading
import json
from utils.relogio_logico import RelogioLogico
from crypto.criptografia import Criptografia

class ClienteBus:
    def __init__(self):
        self.relogio = RelogioLogico()
        self.seguranca = Criptografia()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nome = ""

    def receber(self):
        while True:
            data = self.socket.recv(4096)
            if not data: break
            p = json.loads(data.decode('utf-8'))
            self.relogio.sincronizar(p['tp'])
            
            msg = self.seguranca.decriptar(p['msg'])
            print(f"\n[Recebido de {p['prod']} | T:{p['tp']}]: {msg}")

    def conectar(self):
        self.socket.connect(('127.0.0.1', 5000))
        self.nome = input("Nome: ")
        self.socket.sendall(json.dumps({'acao': 'registrar', 'nome': self.nome}).encode('utf-8'))
        threading.Thread(target=self.receber, daemon=True).start()
        
        while True:
            print("\n=== SISTEMA DE MENSAGENS ===")
            print("1. Enviar Mensagem")
            print("0. Sair")
            
            opcao = input("Opção: ").strip()
            
            if opcao == "1":
                dest = input("Destinatário: ")
                txt = input("Mensagem: ")
                tp = self.relogio.incrementar()
                
                p = {'acao': 'enviar', 'tipo': 'unicast', 'dest': dest, 'prod': self.nome, 'tp': tp, 'msg': self.seguranca.encriptar(txt)}
                self.socket.sendall(json.dumps(p).encode('utf-8'))
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    ClienteBus().conectar()