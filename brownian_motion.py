import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class BrownianRobot:

    def __init__(self, arena_size, start_position=(0.5, 0.5), start_angle=0):
        self.arena_size = arena_size
        self.position = np.array(start_position) * arena_size
        self.angle = start_angle

    def move(self, dt, rotation_std=0.5, max_speed=2.0):

        # if (0 <= self.position[0] <= self.arena_size and
        #     0 <= self.position[1] <= self.arena_size):
        #     # If not hitting a wall, keep current position
        #     return

        # Random rotation
        rotation = random.gauss(0, rotation_std)
        self.angle += rotation

        # Limit angle between 0 and 2*pi
        self.angle = self.angle % (2 * np.pi)

        # Movement vector based on current angle
        movement = np.array([np.cos(self.angle), np.sin(self.angle)]) * max_speed * dt

        # Check for boundary collisions and adjust movement if necessary
        if self.position[0] + movement[0] < 0:
            movement[0] = -self.position[0]
        elif self.position[0] + movement[0] > self.arena_size:
            movement[0] = self.arena_size - self.position[0]
        if self.position[1] + movement[1] < 0:
            movement[1] = -self.position[1]
        elif self.position[1] + movement[1] > self.arena_size:
            movement[1] = self.arena_size - self.position[1]

        # Update robot position
        self.position += movement

def simulate_brownian_motion(arena_size, num_steps, dt, video_filename=None):
    robot = BrownianRobot(arena_size)
    positions = [robot.position.copy()]

    for _ in range(num_steps):
        robot.move(dt)
        positions.append(robot.position.copy())

    if video_filename:
        fig, ax = plt.subplots()
        arena = plt.Rectangle((0, 0), arena_size, arena_size, color='lightgray')
        robot_circle, = ax.plot([], [], 'o', color='red', markersize=10)
        ax.set_aspect('equal')
        ax.add_patch(arena)
        ax.set_xlim(0, arena_size)
        ax.set_ylim(0, arena_size)
        ax.set_title('Brownian Motion Simulation')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        def init():
            robot_circle.set_data([], [])
            return robot_circle,

        def animate(i):
            robot.move(dt)
            positions.append(robot.position.copy())
            robot_circle.set_data(positions[i][0], positions[i][1])
            return robot_circle,

        anim = FuncAnimation(fig, animate, init_func=init, frames=num_steps, interval=10)
        anim.save(video_filename, fps=30)
        plt.close


if __name__ == "__main__":
    simulate_brownian_motion(arena_size=5.0, num_steps=2500, dt=0.01, video_filename="brownian_motion.mp4")