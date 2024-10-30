from pico2d import get_time

class State:
    def enter(self, obj):
        pass

    def exit(self, obj):
        pass

    def do(self, obj):
        pass


class IdleState(State):
    def enter(self, boy):
        boy.frame = 0

    def do(self, boy):
        pass

    def exit(self, boy):
        pass


class RunState(State):
    def enter(self, boy):
        boy.frame = 0

    def do(self, boy):
        boy.x += boy.direction * 5
        boy.frame = (boy.frame + 1) % 8

    def exit(self, boy):
        pass

class AutoRunState(State):
    def enter(self, boy):
        boy.auto_run_start_time = get_time()
        boy.speed = 5
        boy.scale = 1.0
        boy.direction = boy.last_direction
        boy.frame = 0

    def do(self, boy):
        boy.x += boy.direction * boy.speed
        boy.speed += 0.05
        boy.scale += 0.01

        if boy.x <= 0:
            boy.direction = 1
            boy.last_direction = 1
        elif boy.x >= 800:
            boy.direction = -1
            boy.last_direction = -1

        boy.frame = (boy.frame + 1) % 8

        if get_time() - boy.auto_run_start_time > 5:
            boy.state_machine.change_state(IdleState())

    def exit(self, boy):
        boy.speed = 5
        boy.scale = 1.0

class StateMachine:
    def __init__(self, obj):
        self.obj = obj
        self.state = None

    def change_state(self, new_state):
        if self.state is not None:
            self.state.exit(self.obj)
        self.state = new_state
        self.state.enter(self.obj)

    def update(self):
        if self.state is not None:
            self.state.do(self.obj)