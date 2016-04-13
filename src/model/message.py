class MSG:
    # message from, message to, message hashtags and message
    def __init__(self, m_from, m_to, content):
        self.mfrom = m_from
        self.to = m_to
        self.hashtags = []
        self.text = content
        self._extract_hashtags()

    def _extract_hashtags(self):
        words = self.msg.split(' ')
        for word in words:
            if word[0] == '#':
                self.hashtags.append(word[1:])
