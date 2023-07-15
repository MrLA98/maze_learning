from gen_maze import gen_maze
import pygame
import sys


class Point:
    def __init__(self, r, c) -> None:
        self.r = r
        self.c = c

    def __str__(self) -> str:
        return f"({self.r},{self.c})"


class Maze:
    VISUAL_SIZE = 1000

    def __init__(self, size: int, flag: str = "dfs") -> None:
        self.maze_size = 2 * size + 1
        self.maze = gen_maze(size, flag)
        self.start = Point(1, 0)
        self.end = Point(size-2, size)
        self.agent = self.start

    def start_game(self, train: bool = True, visual: bool = True):
        self.train = train
        self.visual = visual
        self.pygame_init()

        while True:
            self.handle_events()
            self.update_screen()

            if self.agent == self.end:
                break

        print("success")
        if self.visual:
            pygame.quit()

    def update_agent_pos(self, down, right):
        r = self.agent.r + down
        c = self.agent.c + right
        if r < 0 or r >= self.maze_size:
            return
        if c < 0 or c >= self.maze_size:
            return
        if self.maze[r][c] != 0:
            return
        self.agent.r = r
        self.agent.c = c

    # ------------------------------ for visual ------------------------------
    def pygame_init(self):
        if self.visual == False:
            return
        pygame.init()
        self.get_pixel()
        self.screen = pygame.display.set_mode(
            (self.screen_size, self.screen_size))

    def handle_events(self):
        if self.visual == False:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.train == False and event.type == pygame.KEYDOWN:
                # 按下键盘按键
                if event.key == pygame.K_LEFT:
                    self.update_agent_pos(0, -1)
                elif event.key == pygame.K_RIGHT:
                    self.update_agent_pos(0, 1)
                elif event.key == pygame.K_UP:
                    self.update_agent_pos(-1, 0)
                elif event.key == pygame.K_DOWN:
                    self.update_agent_pos(1, 0)

    def update_screen(self):
        if self.visual == False:
            return
        self.screen.fill((255, 255, 255))
        self.draw_maze()
        self.draw_agent()
        pygame.display.flip()

    # ------------------------------ visual tools ------------------------------
    def get_pixel(self):
        self.cell_size = 1
        diff = abs(Maze.VISUAL_SIZE - self.cell_size * self.maze_size)
        for i in range(2, 20):
            new_diff = abs(Maze.VISUAL_SIZE - self.maze_size * i)
            if new_diff < diff:
                self.cell_size, diff = i, new_diff
        self.screen_size = self.cell_size * self.maze_size
        print(
            f"screen:{self.screen_size}, cell:{self.cell_size}, maze:{self.maze_size}")

    def draw_rect(self, r, c, color):
        rect = pygame.Rect(c * self.cell_size, r *
                           self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect)

    def draw_maze(self):
        for r in range(self.maze_size):
            for c in range(self.maze_size):
                if self.maze[r][c] == 1:  # 墙壁
                    self.draw_rect(r, c, (0, 0, 0))
                elif self.maze[r][c] == 2:  # 起点
                    self.draw_rect(r, c, (0, 255, 0))
                elif self.maze[r][c] == 3:  # 终点
                    self.draw_rect(r, c, (255, 0, 0))

    def draw_agent(self):
        self.draw_rect(self.agent.r, self.agent.c, (0, 0, 255))


if __name__ == "__main__":
    maze_game = Maze(50, "prim")
    maze_game.start_game(train=False)
