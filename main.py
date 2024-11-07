import pygame
import sys
from ludo.ludo import Ludo
from flappybird.flappybird import FlappyBirdGame
from tetris.tetris import Tetris

class Menu:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    menu_options = ["Ludo", "Tetris", "Flappy Bird", "Quit"]
    font = pygame.font.SysFont(None, 48)
    selected_option = 0
    clock = pygame.time.Clock()
    
    def __init__(self):
        pygame.init()
        self.game_loop()

    def game_loop(self):
        while self.running:
            self.draw_menu(self.selected_option)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            # pygame.quit()
                            Ludo()
                        elif self.selected_option == 1:
                            result = Tetris()
                            if(result == "menu"):
                                continue
                        elif self.selected_option == 2:
                            #FlappyBird()
                            pass
                        elif self.selected_option == 3:
                            pygame.quit()
                            sys.exit()
                        pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

            pygame.display.update()
            self.clock.tick(60)
            

        pygame.quit()

    def draw_menu(self, selected):
        self.screen.fill((0,0,0))
        for i,option in enumerate(self.menu_options):
            if i == selected:
                text = self.font.render(option, True, (255, 255, 255))
            else:
                text = self.font.render(option, True, (100, 100, 100))
            self.screen.blit(text, (self.SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*50))


if __name__ == "__main__":
    Menu()