import pygame
import sys


class Game1:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Game 1")
        clock = pygame.time.Clock()
        self.running = True

        self.player = pygame.Rect(400, 300, 50, 50)
        self.player_speed = 5

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.K_ESCAPE:
                    self.running = False
                    return
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.x -= self.player_speed
            if keys[pygame.K_RIGHT]:
                self.player.x += self.player_speed
            if keys[pygame.K_UP]:
                self.player.y -= self.player_speed
            if keys[pygame.K_DOWN]:
                self.player.y += self.player_speed

            # Update game state
            self.screen.fill((0, 0, 0))  # Clear screen with black
            pygame.draw.rect(self.screen, (255, 0, 0), self.player)  # Draw player

            pygame.display.flip()  # Update display
            clock.tick(60)  # Maintain 60 FPS1

        pygame.quit()
