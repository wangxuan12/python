import constants as const

class GameResult:
    __score = 0
    __life = 0
    __blood = 0

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if value > 0:
            self.__score = value

    def get_max_score(self):
        result = 0
        with open(const.GAME_RESULT_STORE_FILE, 'r') as f:
            r = f.read()
            if r:
                result = int(r)
        return result

    def set_history(self):
        if self.get_max_score() < self.__score:
            with open(const.GAME_RESULT_STORE_FILE, 'w') as f:
                f.write(str(self.__score))
