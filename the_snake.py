from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов с позицией и цветом."""

    def __init__(self):
        """Инициализировать начальную позицию и цвет игрового объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Определить интерфейс отрисовки игрового объекта."""
        raise NotImplementedError(
            'Метод draw должен быть реализован в дочернем классе'
        )


class Apple(GameObject):
    """Яблоко, которое появляется в случайной клетке игрового поля."""

    def __init__(self, occupied_positions=None):
        """Инициализировать яблоко, его цвет и случайную позицию."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Установить случайную позицию яблока в пределах игрового поля."""
        if occupied_positions is None:
            occupied_positions = []
        self.position = None
        while self.position in occupied_positions or self.position is None:
            random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (random_x, random_y)

    # Метод draw класса Apple
    def draw(self):
        """Нарисовать яблоко с рамкой на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка, которая движется, растёт и управляется игроком."""

    def __init__(self):
        """Инициализировать длину, сегменты и направление змейки."""
        super().__init__()
        self.reset()
        self.direction = RIGHT
        self.body_color = SNAKE_COLOR

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Переместить змейку на клетку с учётом границ игрового поля."""
        self.last = None
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        head_x = (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        head_y = (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (head_x, head_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop(-1)

    # Метод draw класса Snake
    def draw(self):
        """Стереть прежний хвост и нарисовать новое положение головы змейки."""
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        head_position = self.get_head_position()
        rect = pygame.Rect(head_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Применить выбранное игроком направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбросить змейку до одного сегмента и выбрать новое направление."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обработать события игры и нажатия клавиш управления."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запустить игровой цикл с движением, столкновениями и отрисовкой."""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
