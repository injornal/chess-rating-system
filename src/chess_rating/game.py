class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def game(self, result):
        player1_rating = self.player1.rating
        if result in (0, 0.5, 1):
            self.player1.rating = self.player1.rating \
                + self.player1.get_k_factor() * (result - self.player1.predict(self.player2.rating))
            self.player2.rating = self.player2.rating \
                + self.player2.get_k_factor() * ((1 - result) - self.player2.predict(player1_rating))
        else:
            raise ValueError("Result is supposed to be 0, 0.5 or 1")
