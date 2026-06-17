from astar import astar
import pygame

pygame.init()

GRID_WIDTH = 600
PANEL_WIDTH = 250

WIDTH = GRID_WIDTH + PANEL_WIDTH
HEIGHT = 600

ROWS = 20
COLS = 20

CELL_SIZE = GRID_WIDTH // COLS

START = (0, 0)
GOAL = (19, 19)

obstacles = set()
path = []

robot_pos = START
robot_index = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Path Planner")

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

clock = pygame.time.Clock()


def draw_grid():

    for row in range(ROWS):

        for col in range(COLS):

            color = (255, 255, 255)

            if (row, col) == robot_pos:
                color = (255, 255, 0)

            elif (row, col) in obstacles:
                color = (0, 0, 0)

            elif (row, col) in path:
                color = (255, 0, 255)

            elif (row, col) == START:
                color = (0, 0, 255)

            elif (row, col) == GOAL:
                color = (0, 255, 0)

            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)


def draw_panel():

    panel_x = GRID_WIDTH

    pygame.draw.rect(
        screen,
        (220, 220, 220),
        (panel_x, 0, PANEL_WIDTH, HEIGHT)
    )

    title = font.render(
        "ROBOT CONTROL",
        True,
        (0, 0, 0)
    )

    screen.blit(title, (panel_x + 20, 20))

    info = [

        "Controls",
        "",
        "Mouse : Add Obstacle",
        "SPACE : Find Path",
        "R : Reset",
        "",
        f"Obstacles : {len(obstacles)}",
        f"Path Length : {len(path)}",
        "",
        "Legend",
        "",
        "Blue   = Start",
        "Green  = Goal",
        "Black  = Wall",
        "Pink   = Path",
        "Yellow = Robot"

    ]

    y = 80

    for text in info:

        line = small_font.render(
            text,
            True,
            (0, 0, 0)
        )

        screen.blit(line, (panel_x + 15, y))

        y += 28


running = True

while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            if x >= GRID_WIDTH:
                continue

            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if (row, col) != START and (row, col) != GOAL:
                obstacles.add((row, col))

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                path = astar(
                    START,
                    GOAL,
                    obstacles,
                    ROWS,
                    COLS
                )

                robot_pos = START
                robot_index = 0

                print("PATH LENGTH =", len(path))

            elif event.key == pygame.K_r:

                obstacles.clear()
                path.clear()

                robot_pos = START
                robot_index = 0

    if len(path) > 0 and robot_index < len(path):

        robot_pos = path[robot_index]
        robot_index += 1

    draw_grid()
    draw_panel()

    pygame.display.flip()

    clock.tick(5)

pygame.quit()