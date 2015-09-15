import pygame

import ai


class Main(object):

    cell_width = 50
    dame_radius = 20
    color = [(240, 30, 0), (20, 20, 40)]
    box_color = (50, 100, 240)

    def __init__(self, table):
        self.table = table
        pygame.init()
        self.screen = pygame.display.set_mode((8 * self.cell_width,
                                               8 * self.cell_width))
        pygame.display.set_caption('Checkers')
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        for row in range(8):
            for col in range(row & 1, 8, 2):
                pygame.draw.rect(self.background, (255, 255, 255),
                                 self.get_rectangle(row, col))
        self.update()

    def get_rectangle(self, row, col):
        return (col * self.cell_width,
                row * self.cell_width,
                self.cell_width,
                self.cell_width),

    def get_center(self, row, col):
        return (col * self.cell_width + self.cell_width / 2,
                row * self.cell_width + self.cell_width / 2)

    def get_row_col(self, pos):
        return pos[1] / self.cell_width, pos[0] / self.cell_width

    def put_dames(self):
        dames_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        for row in range(8):
            for col in range(row & 1, 8, 2):
                if self.table(row, col) != -1:
                    pygame.draw.circle(dames_surface,
                                       self.color[self.table(row, col)],
                                       self.get_center(row, col),
                                       self.dame_radius)
        self.screen.blit(dames_surface, (0, 0))

    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.put_dames()
        pygame.display.flip()

    def run(self):
        start = None
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = self.get_row_col(event.pos)
                if start is None:
                    if self.table(*pos) == self.table.turn:
                        start = pos
                        pygame.draw.rect(self.screen, self.box_color,
                                         self.get_rectangle(start[0], start[1]), 5)
                        pygame.display.flip()
                else:
                    if start == pos:
                        self.update()
                        start = None
                    elif self.table.move(start, pos):
                        self.update()
                        start = None
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                move = ai.play(self.table)
                if move:
                    self.table.unchecked_move(*move)
                    self.update()
