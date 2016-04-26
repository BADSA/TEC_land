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

import json


class Message:
    """
    Plain Old Python Object for storing
    the information of the messages.
    """

    def __init__(self, m_from, m_to, content, type="m"):
        self.m_from = m_from
        self.to = m_to
        self.hashtags = []
        self.text = content
        self.type = type
        self._extract_hash_tags()

    def _extract_hash_tags(self):
        """
        Extracts all the words in the message that begin with "#"
        """
        words = self.text.split(' ')
        self.hashtags = [word for word in words if word[0] == '#']

    def to_dict(self):
        """
        :return: Message information formatted as a dictionary.
        """
        return {
            "message": self.text,
            "from": self.m_from,
            "to": self.to,
            "hashtags": json.dumps(self.hashtags),
            "type": self.type
        }