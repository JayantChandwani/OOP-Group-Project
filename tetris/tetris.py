import random
import pygame
# from main import Menu

pygame.font.init()

class Piece:
    shapes = [
        [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']],
        [['.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0...', '.....']],
        [['.....', '..0..', '..0..', '..0..', '..0..'], ['.....', '0000.', '.....', '.....', '.....']],
        [['.....', '.....', '.00..', '.00..', '.....']],
        [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'],
         ['.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']],
        [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'],
         ['.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']],
        [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'],
         ['.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.00..', '..0..', '.....']]
    ]
    
    shape_colors = [
        (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
        (0, 0, 255), (255, 165, 0), (128, 0, 128)
    ]

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = Piece.shape_colors[Piece.shapes.index(shape)]
        self.rotation = 0


class Tetris:
    col = 10
    row = 20
    s_width = 800
    s_height = 750
    play_width = 300
    play_height = 600
    block_size = 30

    top_left_x = (s_width - play_width) // 2
    top_left_y = s_height - play_height - 50

    filepath = './tetris/highscore.txt'
    fontpath = './tetris/arcade.ttf'
    fontpath_mario = './tetris/mario.ttf'

    def __init__(self):
        self.locked_positions = {}
        self.grid = self.create_grid()
        self.change_piece = False
        self.run = True
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.fall_speed = 0.35
        self.level_time = 0
        self.score = 0
        self.last_score = self.get_max_score()
        self.window = pygame.display.set_mode((Tetris.s_width, Tetris.s_height))
        pygame.display.set_caption('Tetris')
        self.main()

    def create_grid(self):
        grid = [[(0, 0, 0) for _ in range(Tetris.col)] for _ in range(Tetris.row)]
        for y in range(Tetris.row):
            for x in range(Tetris.col):
                if (x, y) in self.locked_positions:
                    color = self.locked_positions[(x, y)]
                    grid[y][x] = color
        return grid

    def convert_shape_format(self, piece):
        positions = []
        shape_format = piece.shape[piece.rotation % len(piece.shape)]
        for i, line in enumerate(shape_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((piece.x + j, piece.y + i))
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
        return positions

    def valid_space(self, piece):
        accepted_pos = [[(x, y) for x in range(Tetris.col) if self.grid[y][x] == (0, 0, 0)] for y in range(Tetris.row)]
        accepted_pos = [x for item in accepted_pos for x in item]
        formatted_shape = self.convert_shape_format(piece)
        for pos in formatted_shape:
            if pos not in accepted_pos:
                if pos[1] >= 0:
                    return False
        return True

    def check_lost(self):
        for pos in self.locked_positions:
            if pos[1] < 1:
                return True
        return False

    def get_shape(self):
        return Piece(5, 0, random.choice(Piece.shapes))

    def draw_text_middle(self, text, size, color, surface):
        font = pygame.font.Font(Tetris.fontpath, size)
        label = font.render(text, 1, color)
        surface.blit(label, (Tetris.top_left_x + Tetris.play_width / 2 - label.get_width() / 2,
                             Tetris.top_left_y + Tetris.play_height / 2 - label.get_height() / 2))

    def draw_grid(self, surface):
        grid_color = (128, 128, 128)
        for i in range(Tetris.row):
            pygame.draw.line(surface, grid_color, (Tetris.top_left_x, Tetris.top_left_y + i * Tetris.block_size),
                             (Tetris.top_left_x + Tetris.play_width, Tetris.top_left_y + i * Tetris.block_size))
            for j in range(Tetris.col):
                pygame.draw.line(surface, grid_color, (Tetris.top_left_x + j * Tetris.block_size, Tetris.top_left_y),
                                 (Tetris.top_left_x + j * Tetris.block_size, Tetris.top_left_y + Tetris.play_height))

    def clear_rows(self):
        increment = 0
        for i in range(len(self.grid) - 1, -1, -1):
            if (0, 0, 0) not in self.grid[i]:
                increment += 1
                index = i
                for j in range(len(self.grid[i])):
                    try:
                        del self.locked_positions[(j, i)]
                    except ValueError:
                        continue
        if increment > 0:
            for key in sorted(list(self.locked_positions), key=lambda a: a[1])[::-1]:
                x, y = key
                if y < index:
                    new_key = (x, y + increment)
                    self.locked_positions[new_key] = self.locked_positions.pop(key)
        return increment

    def draw_next_shape(self, piece, surface):
        font = pygame.font.Font(Tetris.fontpath, 30)
        label = font.render('Next shape', 1, (255, 255, 255))
        start_x = Tetris.top_left_x + Tetris.play_width + 50
        start_y = Tetris.top_left_y + (Tetris.play_height / 2 - 100)
        shape_format = piece.shape[piece.rotation % len(piece.shape)]
        for i, line in enumerate(shape_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, piece.color, (start_x + j * Tetris.block_size, start_y + i * Tetris.block_size, Tetris.block_size, Tetris.block_size), 0)
        surface.blit(label, (start_x, start_y - 30))

    def draw_window(self, surface):
        surface.fill((0, 0, 0))
        font = pygame.font.Font(Tetris.fontpath_mario, 65)
        label = font.render('TETRIS', 1, (255, 255, 255))
        surface.blit(label, (Tetris.top_left_x + Tetris.play_width / 2 - label.get_width() / 2, 30))
        font = pygame.font.Font(Tetris.fontpath, 30)
        label = font.render('SCORE   ' + str(self.score), 1, (255, 255, 255))
        surface.blit(label, (Tetris.top_left_x + Tetris.play_width + 50, Tetris.top_left_y + Tetris.play_height / 2 - 100 + 200))
        label_hi = font.render('HIGHSCORE   ' + str(self.last_score), 1, (255, 255, 255))
        surface.blit(label_hi, (Tetris.top_left_x - 240, Tetris.top_left_y + 200))

        for i in range(Tetris.row):
            for j in range(Tetris.col):
                pygame.draw.rect(surface, self.grid[i][j], (Tetris.top_left_x + j * Tetris.block_size, Tetris.top_left_y + i * Tetris.block_size, Tetris.block_size, Tetris.block_size), 0)

        # Draw the current piece on the grid
        formatted_shape = self.convert_shape_format(self.current_piece)
        for pos in formatted_shape:
            x, y = pos
            if y > -1:
                pygame.draw.rect(surface, self.current_piece.color,
                                 (Tetris.top_left_x + x * Tetris.block_size, Tetris.top_left_y + y * Tetris.block_size, Tetris.block_size, Tetris.block_size), 0)

        self.draw_grid(surface)

    def lock_piece(self):
        formatted = self.convert_shape_format(self.current_piece)
        for pos in formatted:
            p = (pos[0], pos[1])
            self.locked_positions[p] = self.current_piece.color
        self.current_piece = self.next_piece
        self.next_piece = self.get_shape()
        self.change_piece = False
        self.score += self.clear_rows() * 10

    def get_max_score(self):
        with open(Tetris.filepath, 'r') as f:
            return int(f.readline().strip())

    def update_score(self):
        high_score = self.get_max_score()
        if self.score > high_score:
            with open(Tetris.filepath, 'w') as f:
                f.write(str(self.score))

    def show_game_over_screen(self):

        game_over_font = pygame.font.SysFont(None, 125, bold=True)
        instruction_font = pygame.font.SysFont(None, 24)
        score_font = pygame.font.SysFont(None, 32, bold=True)
        
        game_over_surface = game_over_font.render('Game Over', True, (255, 0, 0))
        score_surface = score_font.render(f'Score: {self.score}', True, (255, 255, 255))

        instruction_text = 'Press SPACE to restart and ESC to return to main menu'
        instruction_surface = instruction_font.render(instruction_text, True, (255, 255, 255))

        game_over_x = self.s_width / 2 - game_over_surface.get_width() / 2
        game_over_y = self.s_height / 2 - game_over_surface.get_height()
        score_x = self.s_width / 2 - score_surface.get_width() / 2
        score_y = game_over_y + game_over_surface.get_height() + 10
        instruction_x = self.s_width / 2 - instruction_surface.get_width() / 2
        instruction_y = self.s_height - instruction_surface.get_height() - 20

        self.window.fill((0, 0, 0))
        self.window.blit(game_over_surface, (game_over_x, game_over_y))
        self.window.blit(score_surface, (score_x, score_y))
        self.window.blit(instruction_surface, (instruction_x, instruction_y))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    # pygame.quit()
                    if(event.type == pygame.QUIT):
                        sys.exit()
                    return "menu"
                elif event.type == pygame.KEYUP:
                    self.__init__()
                    return

    def main(self):
        self.grid = self.create_grid()
        while self.run:
            self.grid = self.create_grid()
            self.fall_time += self.clock.get_rawtime()
            self.level_time += self.clock.get_rawtime()
            self.clock.tick()
            if self.level_time / 1000 > 5:
                self.level_time = 0
                if self.fall_speed > 0.15:
                    self.fall_speed -= 0.005
            if self.fall_time / 1000 >= self.fall_speed:
                self.fall_time = 0
                self.current_piece.y += 1
                if not self.valid_space(self.current_piece) and self.current_piece.y > 0:
                    self.current_piece.y -= 1
                    self.lock_piece()
                    self.change_piece = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.display.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.x -= 1
                        if not self.valid_space(self.current_piece):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece.x += 1
                        if not self.valid_space(self.current_piece):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        self.current_piece.y += 1
                        if not self.valid_space(self.current_piece):
                            self.current_piece.y -= 1
                    elif event.key == pygame.K_UP:
                        self.current_piece.rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)
                        if not self.valid_space(self.current_piece):
                            self.current_piece.rotation = (self.current_piece.rotation - 1) % len(self.current_piece.shape)
            self.draw_window(self.window)
            self.draw_next_shape(self.next_piece, self.window)
            pygame.display.update()
            if self.check_lost():
                self.run = False
                self.update_score()
                # self.draw_text_middle("YOU LOST!", 40, (255, 255, 255), self.window)
                # pygame.display.update()
                # pygame.time.delay(1500)
                # pygame.quit()
                return self.show_game_over_screen()
                # Menu()
                # quit()


if __name__ == '__main__':
    tetris = Tetris()
    tetris.main()
