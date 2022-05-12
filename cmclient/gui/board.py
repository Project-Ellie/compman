import pygame

from cmclient.api.basics import string_to_stones
from cmclient.gui.emitter import BoardEventEmitter


COLOR_BOARD = (50, 80, 70)
COLOR_WHITE = (255, 255, 255)
COLOR_WHITE_STONES = (200, 255, 255)
COLOR_BLACK_STONES = (0, 20, 20)
STONE_COLORS = [COLOR_BLACK_STONES, COLOR_WHITE_STONES]

GRID_SIZE = 45
BOARD_SIZE = 15
MIDDLE = BOARD_SIZE // 2 + 1
SIDE_BUFFER = 30
WH = GRID_SIZE * (BOARD_SIZE + 1) + 2 * SIDE_BUFFER
PHYSICAL_BOARD = [WH] * 2
PADDING = GRID_SIZE + SIDE_BUFFER

TIME_DELAY = 500
POLL_NOW = pygame.USEREVENT + 1


def show(registered: str, oppenent: str, state: str,
         move_listener, polling_listener):
    pygame.init()
    pygame.time.set_timer(POLL_NOW, TIME_DELAY)
    screen = pygame.display.set_mode(PHYSICAL_BOARD)
    screen.fill(COLOR_BOARD)
    pygame.display.set_caption(f"{registered} vs {oppenent}")
    draw_grid(screen)
    draw_field_names(screen)
    current_color = 0
    if state is not None:
        current_color = draw_stones(screen, state)

    pygame.display.update()
    loop(move_listener, polling_listener, screen, current_color)

    return "Done."


def draw_field_names(screen):
    for i in range(1, BOARD_SIZE + 1):

        char = chr(64 + i)
        draw_text(screen, char,
                  GRID_SIZE * i + SIDE_BUFFER, WH-GRID_SIZE//2, COLOR_WHITE, 16)
        draw_text(screen, char,
                  GRID_SIZE * i + SIDE_BUFFER, GRID_SIZE//2, COLOR_WHITE, 16)

        char = str(BOARD_SIZE + 1 - i)
        draw_text(screen, char,
                  WH-GRID_SIZE//2, GRID_SIZE * i + SIDE_BUFFER, COLOR_WHITE, 16)
        draw_text(screen, char,
                  GRID_SIZE//2, GRID_SIZE * i + SIDE_BUFFER, COLOR_WHITE, 16)


def draw_grid(screen):

    for i in range(1, BOARD_SIZE + 1):
        pygame.draw.line(screen, COLOR_WHITE,
                         [GRID_SIZE * i + SIDE_BUFFER, GRID_SIZE + SIDE_BUFFER],
                         [GRID_SIZE * i + SIDE_BUFFER, BOARD_SIZE * GRID_SIZE + SIDE_BUFFER], 2)
        pygame.draw.line(screen, COLOR_WHITE,
                         [GRID_SIZE + SIDE_BUFFER, GRID_SIZE * i + SIDE_BUFFER],
                         [BOARD_SIZE * GRID_SIZE + SIDE_BUFFER, GRID_SIZE * i + SIDE_BUFFER], 2)

    pygame.draw.circle(screen, COLOR_WHITE,
                       [GRID_SIZE * MIDDLE + SIDE_BUFFER,
                        GRID_SIZE * MIDDLE + SIDE_BUFFER], 8)


def draw_text(screen, text, x_pos, y_pos, font_color, font_size):
    ff = pygame.font.Font(pygame.font.get_default_font(), font_size)
    surface, rect = text_objects(text, ff, font_color)
    rect.center = (x_pos, y_pos)
    screen.blit(surface, rect)


def text_objects(text, font, font_color):
    surface = font.render(text, True, font_color)
    return surface, surface.get_rect()


def draw_stones(screen, state: str):
    stones = string_to_stones(state)
    color = 0
    for stone in stones:
        if stone is not None:  # there may be 'non-moves'
            draw_stone(screen, stone, STONE_COLORS[color])
            color = 1 - color
    return color


def draw_stone(screen, pos, color):
    bx, by = pos
    x = (ord(bx) - 65) * GRID_SIZE + PADDING
    y = (BOARD_SIZE - by) * GRID_SIZE + PADDING
    pygame.draw.circle(screen, color,
                       (x, y), GRID_SIZE // 2 - 1)
    pygame.display.update()


def loop(move_listener, polling_listener, screen, current_color):
    emitter = BoardEventEmitter(PADDING, BOARD_SIZE, GRID_SIZE, [POLL_NOW])
    ongoing = True
    while ongoing:
        event = emitter.get()
        if event == "EXIT":
            ongoing = False
        elif event == POLL_NOW:
            other_move = polling_listener()
            if other_move is not None:
                bx, by = other_move
                draw_stone(screen, (bx, by), STONE_COLORS[current_color])
                current_color = 1 - current_color
        else:
            my_move = move_listener(event)
            if my_move is not None:  # move may be illegal
                bx, by = string_to_stones(my_move)[0]
                draw_stone(screen, (bx, by), STONE_COLORS[current_color])
                current_color = 1 - current_color

    return "Done playing."
