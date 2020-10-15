from game.war import AirWar
import constants as const

def main():
    war = AirWar()
    war.add_small_enemies(const.SMALL_ENEMY_NUM)
    war.run_game()

if __name__ == '__main__':
    main()