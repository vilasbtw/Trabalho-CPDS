import base64

class Criptografia:
    def __init__(self):
        self.encoding = 'utf-8'

    def encriptar(self, mensagem):
        # Transforma a string em bytes
        msg_bytes = mensagem.encode(self.encoding)
        # Codifica em Base64 (simulando a cifragem para o transporte)
        b64_bytes = base64.b64encode(msg_bytes)
        return b64_bytes.decode(self.encoding)

    def decriptar(self, mensagem_encriptada):
        # Transforma a string Base64 de volta em bytes
        b64_bytes = mensagem_encriptada.encode(self.encoding)
        # Decodifica o Base64
        msg_bytes = base64.b64decode(b64_bytes)
        return msg_bytes.decode(self.encoding)