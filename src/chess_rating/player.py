class Player:
    _k_factor = 16

    def __init__(self, rating=1000):
        self.rating = rating

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = round(value)

    def predict(self, opponent_rating):
        return 1 / (1 + 10 ** ((opponent_rating - self.rating) / 400))

    def get_k_factor(self):
        return self._k_factor
