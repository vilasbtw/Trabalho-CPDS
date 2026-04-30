import unittest
from unittest.mock import MagicMock
import threading
import os
import json

from utils.relogio_logico import RelogioLogico
from crypto.criptografia import Criptografia
from server.message_buffer import MessageBus

class TestSistemaMensageria(unittest.TestCase):

    def test_01_criptografia(self):
        crypto = Criptografia()
        texto_original = "Olá Professor"
        cifrado = crypto.encriptar(texto_original)
        self.assertNotEqual(texto_original, cifrado)
        decifrado = crypto.decriptar(cifrado)
        self.assertEqual(texto_original, decifrado)

    def test_02_relogio_logico_incremento(self):
        relogio = RelogioLogico()
        self.assertEqual(relogio.incrementar(), 1)
        self.assertEqual(relogio.incrementar(), 2)

    def test_03_relogio_logico_sincronizacao(self):
        relogio = RelogioLogico()
        relogio.incrementar()
        relogio.incrementar()
        relogio.sincronizar(5)
        self.assertEqual(relogio.tempo, 6)

    def test_04_concorrencia_exclusao_mutua(self):
        relogio = RelogioLogico()
        threads = []
        
        def tarefa():
            for _ in range(100):
                relogio.incrementar()
                
        for _ in range(50):
            t = threading.Thread(target=tarefa)
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        self.assertEqual(relogio.tempo, 5000)

    def test_05_auditoria_log(self):
        bus = MessageBus()
        log_msg = "[T:1] Alice -> Bob [T:2] | Conteúdo: Ola"
        bus.registrar_log(log_msg)
        
        self.assertTrue(os.path.exists('server/auditoria_log.txt'))
        with open('server/auditoria_log.txt', 'r', encoding='utf-8') as f:
            conteudo = f.read()
        self.assertIn(log_msg, conteudo)

    def test_06_roteamento_unicast(self):
        bus = MessageBus()
        mock_alice = MagicMock()
        mock_bob = MagicMock()
        bus.clientes = {'Alice': mock_alice, 'Bob': mock_bob}
        
        p = {'acao': 'enviar', 'tipo': 'unicast', 'dest': 'Bob', 'prod': 'Alice', 'tp': 1, 'msg': 'teste'}
        mock_alice.recv.side_effect = [json.dumps(p).encode('utf-8'), b'']
        
        bus.tratar_cliente(mock_alice, ('127.0.0.1', 12345))
        
        mock_bob.sendall.assert_called_once()
        args, _ = mock_bob.sendall.call_args
        enviado = json.loads(args[0].decode('utf-8'))
        self.assertEqual(enviado['dest'], 'Bob')

    def test_07_roteamento_multicast(self):
        bus = MessageBus()
        mock_alice = MagicMock()
        mock_bob = MagicMock()
        mock_carol = MagicMock()
        bus.clientes = {'Alice': mock_alice, 'Bob': mock_bob, 'Carol': mock_carol}
        bus.canais = {'TI': ['Alice', 'Bob']}
        
        p = {'acao': 'enviar', 'tipo': 'multicast', 'dest': 'TI', 'prod': 'Carol', 'tp': 1, 'msg': 'aviso'}
        mock_carol.recv.side_effect = [json.dumps(p).encode('utf-8'), b'']
        
        bus.tratar_cliente(mock_carol, ('127.0.0.1', 12345))
        
        mock_alice.sendall.assert_called_once()
        mock_bob.sendall.assert_called_once()
        mock_carol.sendall.assert_not_called()

    def test_08_roteamento_broadcast(self):
        bus = MessageBus()
        mock_alice = MagicMock()
        mock_bob = MagicMock()
        bus.clientes = {'Alice': mock_alice, 'Bob': mock_bob}
        
        p = {'acao': 'enviar', 'tipo': 'broadcast', 'dest': 'todos', 'prod': 'Alice', 'tp': 1, 'msg': 'geral'}
        mock_alice.recv.side_effect = [json.dumps(p).encode('utf-8'), b'']
        
        bus.tratar_cliente(mock_alice, ('127.0.0.1', 12345))
        
        mock_alice.sendall.assert_called_once()
        mock_bob.sendall.assert_called_once()

if __name__ == '__main__':
    unittest.main()