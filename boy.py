from pico2d import *
from state_machine import StateMachine, IdleState, RunState, AutoRunState

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.direction = 0
        self.last_direction = 1
        self.scale = 1.0
        self.speed = 5

        self.state_machine = StateMachine(self)
        self.state_machine.change_state(IdleState())

    def update(self):
        self.state_machine.update()

        self.x = clamp(0, self.x, 800)

    def draw(self):
        if isinstance(self.state_machine.state, RunState):
            if self.direction == 1:
                self.last_direction = 1
                self.image.clip_draw(self.frame * 100, 100 * 1, 100, 100, self.x, self.y)
            elif self.direction == -1:
                self.last_direction = -1
                self.image.clip_draw(self.frame * 100, 100 * 0, 100, 100, self.x, self.y)
        elif isinstance(self.state_machine.state, AutoRunState):
            adjusted_y = self.y + (self.scale - 1) * (30)
            if self.last_direction == 1:
                self.image.clip_draw(
                    self.frame * 100, 100 * 1, 100, 100,
                    self.x, adjusted_y,
                    100 * self.scale, 100 * self.scale
                )
            else:
                self.image.clip_draw(
                    self.frame * 100, 100 * 0, 100, 100,
                    self.x, adjusted_y,
                    100 * self.scale, 100 * self.scale
                )
        elif isinstance(self.state_machine.state, IdleState):
            if self.last_direction == 1:
                self.image.clip_draw(0, 100 * 3, 100, 100, self.x, self.y)
            elif self.last_direction == -1:
                self.image.clip_draw(0, 100 * 2, 100, 100, self.x, self.y)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.direction = 1
                self.state_machine.change_state(RunState())
            elif event.key == SDLK_LEFT:
                self.direction = -1
                self.state_machine.change_state(RunState())
            elif event.key == SDLK_a:
                self.state_machine.change_state(AutoRunState())
        elif event.type == SDL_KEYUP:
            if (event.key == SDLK_RIGHT and self.direction == 1) or \
                    (event.key == SDLK_LEFT and self.direction == -1):
                self.direction = 0
                self.state_machine.change_state(IdleState())