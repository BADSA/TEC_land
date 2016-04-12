class MSG:

    # message from, message to, message hashtags and message
    def __init__(self, m_from, m_to, msg):
        self.m_from = m_from
        self._to = m_to
        self.hashtags = []
        self.msg = msg
        self._subtract_messages()

    def _subtract_messages(self):
        words = self.msg.split(' ')
        for word in words:
            if word[0] == '#':
                self.hashtags.append(word[:1])
