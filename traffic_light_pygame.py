# traffic_light_pygame.py
import pygame
import time
from traffic_light_system import TrafficLightSystem  # << importing your classes

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Light Simulation")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)

# Define light positions
light_positions = [(WIDTH // 2, 100), (WIDTH // 2, 250), (WIDTH // 2, 400)]

clock = pygame.time.Clock()

def draw_traffic_light(state):
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, (WIDTH//2 - 40, 50, 80, 400))

    if state == "RED":
        pygame.draw.circle(screen, RED, light_positions[0], 30)
        pygame.draw.circle(screen, BLACK, light_positions[1], 30)
        pygame.draw.circle(screen, BLACK, light_positions[2], 30)
    elif state == "YELLOW":
        pygame.draw.circle(screen, BLACK, light_positions[0], 30)
        pygame.draw.circle(screen, YELLOW, light_positions[1], 30)
        pygame.draw.circle(screen, BLACK, light_positions[2], 30)
    elif state == "GREEN":
        pygame.draw.circle(screen, BLACK, light_positions[0], 30)
        pygame.draw.circle(screen, BLACK, light_positions[1], 30)
        pygame.draw.circle(screen, GREEN, light_positions[2], 30)

    pygame.display.update()

def next_state(current_state):
    if current_state == "RED":
        return "GREEN"
    elif current_state == "GREEN":
        return "YELLOW"
    elif current_state == "YELLOW":
        return "RED"

def main():
    api_key = "AIzaSyD417P0pS9mbGiKf3ZZHrqHAOhyV2l90fg"  # Replace this with your actual key
    locations = ["New York, NY"]  # You can add more if you want
    system = TrafficLightSystem(locations, api_key)

    running = True
    last_switch = time.time()
    light_index = 0  # pick first light

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Adjust light timing every cycle based on traffic
        system.adjust_light_timings()

        current_light = system.lights[light_index]
        draw_traffic_light(current_light.state)

        # Switch light after its current time
        if time.time() - last_switch > current_light.get_current_duration():
            current_light.update_state()
            last_switch = time.time()

    pygame.quit()

if __name__ == "__main__":
    main()
