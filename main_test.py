import pygame
import sys

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load your games (assuming they are in separate files)
from Game1 import Game1
# from game2 import run_game2
# from game3 import run_game3

# Menu options
font = pygame.font.SysFont(None, 48)
menu_options = ['Play Game 1', 'Play Game 2', 'Play Game 3', 'Quit']

def draw_menu(selected):
    screen.fill((0, 0, 0))
    for i, option in enumerate(menu_options):
        if i == selected:
            text = font.render(option, True, (255, 255, 255))
        else:
            text = font.render(option, True, (100, 100, 100))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i * 50))

def main():
    selected_option = 0
    clock = pygame.time.Clock()

    while True:
        draw_menu(selected_option)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        Game1()
                    elif selected_option == 1:
                        # run_game2()
                        pass
                    elif selected_option == 2:
                        # run_game3()
                        pass
                    elif selected_option == 3:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
