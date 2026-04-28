import threading

class RelogioLogico:
    def __init__(self):
        self.tempo = 0
        self.mutex = threading.Lock()

    def incrementar(self):
        with self.mutex:
            self.tempo += 1
            return self.tempo

    def sincronizar(self, tempo_recebido):
        with self.mutex:
            self.tempo = max(self.tempo, tempo_recebido) + 1
            return self.tempo