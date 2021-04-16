class Challenge:
    """
    Individual challenges to do
    """

    def __init__(self, description='get up and stretch', timeout=60):
        self.timeout = timeout
        self.description = description

    def __str__(self):
        timeout_str = f'You have {self.timeout}s to finish this task.'
        return f'{timeout_str}\n{self.description}'

    def get_timeout(self):
        return self.timeout
