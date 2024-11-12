#! /usr/bin/env python3
"""Flappy Bird, refactored to match game1 structure."""

import math
import os
from random import randint
from collections import deque
import sys

import pygame
from pygame.locals import *


FPS = 60
ANIMATION_SPEED = 0.18  # pixels per millisecond
WIN_WIDTH = 284 * 2     # BG image size: 284x512 px; tiled twice
WIN_HEIGHT = 512


class Bird(pygame.sprite.Sprite):
    WIDTH = HEIGHT = 32
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.3
    CLIMB_DURATION = 333.3

    def __init__(self, x, y, msec_to_climb, images):
        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

    def update(self, delta_frames=1):
        if self.msec_to_climb > 0:
            frac_climb_done = 1 - self.msec_to_climb / Bird.CLIMB_DURATION
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames) *
                       (1 - math.cos(frac_climb_done * math.pi)))
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)

    @property
    def image(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wingup
        else:
            return self._img_wingdown

    @property
    def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

    @property
    def rect(self):
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)


class PipePair(pygame.sprite.Sprite):
    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000

    def __init__(self, pipe_end_img, pipe_body_img):
        self.x = float(WIN_WIDTH - 1)
        self.score_counted = False
        self.image = pygame.Surface((PipePair.WIDTH, WIN_HEIGHT), SRCALPHA)
        self.image.convert()
        self.image.fill((0, 0, 0, 0))
        total_pipe_body_pieces = int((WIN_HEIGHT - 3 * Bird.HEIGHT - 3 * PipePair.PIECE_HEIGHT) / PipePair.PIECE_HEIGHT)
        self.bottom_pieces = randint(1, total_pipe_body_pieces)
        self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

        for i in range(1, self.bottom_pieces + 1):
            piece_pos = (0, WIN_HEIGHT - i * PipePair.PIECE_HEIGHT)
            self.image.blit(pipe_body_img, piece_pos)
        bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px
        bottom_end_piece_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
        self.image.blit(pipe_end_img, bottom_end_piece_pos)

        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img, (0, i * PipePair.PIECE_HEIGHT))
        top_pipe_end_y = self.top_height_px
        self.image.blit(pipe_end_img, (0, top_pipe_end_y))

        self.top_pieces += 1
        self.bottom_pieces += 1
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def top_height_px(self):
        return self.top_pieces * PipePair.PIECE_HEIGHT

    @property
    def bottom_height_px(self):
        return self.bottom_pieces * PipePair.PIECE_HEIGHT

    @property
    def visible(self):
        return -PipePair.WIDTH < self.x < WIN_WIDTH

    @property
    def rect(self):
        return Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)

    def update(self, delta_frames=1):
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)

    def collides_with(self, bird):
        return pygame.sprite.collide_mask(self, bird)


class FlappyBird:
    """Main game class for Flappy Bird, matching game1 structure."""

    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.SysFont(None, 32, bold=True)
        self.images = self.load_images()
        self.bird = Bird(50, int(WIN_HEIGHT / 2 - Bird.HEIGHT / 2), 2, 
                         (self.images['bird-wingup'], self.images['bird-wingdown']))
        self.pipes = deque()
        self.frame_clock = 0
        self.score = 0
        self.done = False
        self.paused = False
        self.game_loop()

    def load_images(self):
        def load_image(img_file_name):
            file_name = os.path.join(os.path.dirname(__file__), 'images', img_file_name)
            img = pygame.image.load(file_name)
            img.convert()
            return img

        return {
            'background': load_image('background.png'),
            'pipe-end': load_image('pipe_end.png'),
            'pipe-body': load_image('pipe_body.png'),
            'bird-wingup': load_image('bird_wing_up.png'),
            'bird-wingdown': load_image('bird_wing_down.png'),
        }

    
    def show_game_over_screen(self):

        game_over_font = pygame.font.SysFont(None, 125, bold=True)
        instruction_font = pygame.font.SysFont(None, 24)
        
        game_over_surface = game_over_font.render('Game Over', True, (255, 0, 0))
        score_surface = self.score_font.render(f'Score: {self.score}', True, (255, 255, 255))

        instruction_text = 'Press SPACE to restart and ESC to return to main menu'
        instruction_surface = instruction_font.render(instruction_text, True, (255, 255, 255))

        game_over_x = WIN_WIDTH / 2 - game_over_surface.get_width() / 2
        game_over_y = WIN_HEIGHT / 2 - game_over_surface.get_height()
        score_x = WIN_WIDTH / 2 - score_surface.get_width() / 2
        score_y = game_over_y + game_over_surface.get_height() + 10
        instruction_x = WIN_WIDTH / 2 - instruction_surface.get_width() / 2
        instruction_y = WIN_HEIGHT - instruction_surface.get_height() - 20

        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(game_over_surface, (game_over_x, game_over_y))
        self.display_surface.blit(score_surface, (score_x, score_y))
        self.display_surface.blit(instruction_surface, (instruction_x, instruction_y))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    # pygame.quit()
                    if(event.type == QUIT):
                        sys.exit()
                    return "menu"
                elif event.type == KEYUP:
                    self.__init__()
                    return

    def game_loop(self):
        """Main game loop."""
        while not self.done:
            self.clock.tick(FPS)
            
            if not (self.paused or self.frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
                self.pipes.append(PipePair(self.images['pipe-end'], self.images['pipe-body']))

            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    self.done = True
                elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
                    self.paused = not self.paused
                elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and e.key in (K_UP, K_RETURN, K_SPACE)):
                    self.bird.msec_to_climb = Bird.CLIMB_DURATION

            if self.paused:
                continue

            if any(p.collides_with(self.bird) for p in self.pipes) or self.bird.y <= 0 or self.bird.y >= WIN_HEIGHT - Bird.HEIGHT:
                self.done = True

            # Draw the background twice to cover the entire width
            self.display_surface.blit(self.images['background'], (0, 0))
            self.display_surface.blit(self.images['background'], (284, 0))

            while self.pipes and not self.pipes[0].visible:
                self.pipes.popleft()

            for p in self.pipes:
                p.update()
                self.display_surface.blit(p.image, p.rect)

            self.bird.update()
            self.display_surface.blit(self.bird.image, self.bird.rect)

            for p in self.pipes:
                if p.x + PipePair.WIDTH < self.bird.x and not p.score_counted:
                    self.score += 1
                    p.score_counted = True

            score_surface = self.score_font.render(str(self.score), True, (255, 255, 255))
            score_x = WIN_WIDTH / 2 - score_surface.get_width() / 2
            self.display_surface.blit(score_surface, (score_x, PipePair.PIECE_HEIGHT))

            pygame.display.flip()
            self.frame_clock += 1

        print(f'Game over! Score: {self.score}')
        return self.show_game_over_screen()
        # return "menu"
        # pygame.quit()


def frames_to_msec(frames, fps=FPS):
    return 1000.0 * frames / fps


def msec_to_frames(milliseconds, fps=FPS):
    return fps * milliseconds / 1000.0


if __name__ == '__main__':
    game = FlappyBird()
    # game.game_loop()
