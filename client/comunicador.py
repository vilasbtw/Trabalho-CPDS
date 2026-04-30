import socket
import threading
import json
import string
import time
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
            try:
                data = self.socket.recv(4096)
                if not data: break
                p = json.loads(data.decode('utf-8'))
                
                if p.get('acao') == 'erro':
                    print(f"\n[ALERTA DO SISTEMA]: {p['msg']}")
                    print("(Pressione ENTER para atualizar o menu)")
                    continue
                
                self.relogio.sincronizar(p['tp'])
                msg = self.seguranca.decriptar(p['msg'])
                print(f"\n[Recebido de {p['prod']} | T:{p['tp']}]: {msg}")
                print("(Pressione ENTER para atualizar o menu)")
                
                ack = {'acao': 'ack', 'prod': p['prod'], 'tp': p['tp'], 'tc': self.relogio.incrementar(), 'msg': p['msg']}
                self.socket.sendall(json.dumps(ack).encode('utf-8'))
            except:
                break

    def conectar(self):
        self.socket.connect(('127.0.0.1', 5000))
        
        while True:
            nome = input("Nome: ").strip()
            permitidos = string.ascii_letters + string.digits
            if all(c in permitidos for c in nome) and nome != "":
                self.nome = nome
                break
            print("[ALERTA] Nome inválido! Use apenas letras (sem acentos) e números.")

        self.socket.sendall(json.dumps({'acao': 'registrar', 'nome': self.nome}).encode('utf-8'))
        threading.Thread(target=self.receber, daemon=True).start()
        
        while True:
            time.sleep(0.1)
            
            print("\n=== SISTEMA DE MENSAGENS ===")
            print("1. Enviar Mensagem (Unicast)")
            print("2. Enviar para Todos (Broadcast)")
            print("3. Entrar em um Canal")
            print("4. Enviar para um Canal (Multicast)")
            print("0. Sair")
            
            opcao = input("Opção: ").strip()
            
            if opcao == "":
                continue
            
            if opcao == "1":
                dest = input("Destinatário: ")
                txt = input("Mensagem: ")
                
                if len(txt) > 100:
                    print("\n[ALERTA] Mensagem muito longa! Limite de 100 caracteres.")
                    continue
                
                tp = self.relogio.incrementar()
                p = {'acao': 'enviar', 'tipo': 'unicast', 'dest': dest, 'prod': self.nome, 'tp': tp, 'msg': self.seguranca.encriptar(txt)}
                self.socket.sendall(json.dumps(p).encode('utf-8'))
            
            elif opcao == "2":
                txt = input("Mensagem para todos: ")
                
                if len(txt) > 100:
                    print("\n[ALERTA] Mensagem muito longa! Limite de 100 caracteres.")
                    continue
                
                tp = self.relogio.incrementar()
                p = {'acao': 'enviar', 'tipo': 'broadcast', 'dest': 'todos', 'prod': self.nome, 'tp': tp, 'msg': self.seguranca.encriptar(txt)}
                self.socket.sendall(json.dumps(p).encode('utf-8'))
                
            elif opcao == "3":
                canal = input("Nome do Canal: ")
                p = {'acao': 'entrar_canal', 'canal': canal}
                self.socket.sendall(json.dumps(p).encode('utf-8'))
                print(f"\n[SISTEMA] Você entrou no canal '{canal}'.")
                
            elif opcao == "4":
                dest = input("Nome do Canal: ")
                txt = input("Mensagem: ")
                
                if len(txt) > 100:
                    print("\n[ALERTA] Mensagem muito longa! Limite de 100 caracteres.")
                    continue
                
                tp = self.relogio.incrementar()
                p = {'acao': 'enviar', 'tipo': 'multicast', 'dest': dest, 'prod': self.nome, 'tp': tp, 'msg': self.seguranca.encriptar(txt)}
                self.socket.sendall(json.dumps(p).encode('utf-8'))

            elif opcao == "0":
                break
            else:
                print("\nOpção inválida.")

if __name__ == "__main__":
    ClienteBus().conectar()