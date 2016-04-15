# coding=utf-8
"""
Instituto Tecnológico de Costa Rica
Ingeniería en Computación
Redes de Computadoras
Profesor: Kevin Moraga
Estudiantes:
    Daniel Solís Méndez
    Melvin Elizondo Pérez
I Semestre 2016
"""


class Message:

    def __init__(self, m_from, m_to, content):
        self.mfrom = m_from
        self.to = m_to
        self.hashtags = []
        self.text = content
        self._extract_hash_tags()

    def _extract_hash_tags(self):
        words = self.text.split(' ')
        for word in words:
            if word[0] == '#':
                self.hashtags.append(word[1:])
