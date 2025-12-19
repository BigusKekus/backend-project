import pygame
import sys
from model.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BULLET_SPEED
from model.player import Player
from model.star import generate_starfield
from view.font_loader import load_font
from view.renderer import Renderer
from controller.game_controller import GameController
from controller.input_handler import handle_input
from controller.state_manager import StateManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    font = load_font(18)
    state_manager = StateManager()
    player = Player()
    stars = generate_starfield(50)
    renderer = Renderer(screen, font)
    game_controller = GameController(player, BULLET_SPEED, font, state_manager)
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if state_manager.is_main_menu():
                for button in game_controller.menu_buttons:
                    button.handle_event(event)
            elif state_manager.is_paused():
                for button in game_controller.pause_buttons:
                    button.handle_event(event)
            elif state_manager.is_game_over():
                for button in game_controller.game_over_buttons:
                    button.handle_event(event)
            elif state_manager.is_guide():
                for button in game_controller.guide_buttons:
                    button.handle_event(event)
        handle_input(player, state_manager, game_controller, events)
        if state_manager.is_playing() or state_manager.is_next_level():
            game_controller.update()
        renderer.render(state_manager, game_controller, stars)
        clock.tick(FPS)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
