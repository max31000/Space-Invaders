import pygame
import logic
from collections import defaultdict
import config
from objects import Objects
from interface import Interface
import time
import textures
import io_json


class Game:
    """
    Start game and handle class
    """
    def __init__(self):
        """
        declare fields, start game timer
        """
        self.clock = pygame.time.Clock()
        self.surface = None
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.objects = None
        self.level = 1
        self.player = None
        self.player_health = 4
        self.game_mode = None
        self.is_pause = False
        self.save_file = io_json.Json("leaders.json")

    def create_window(self):
        pygame.init()
        self.surface = pygame.display.set_mode((config.width, config.height))

    def create_game(self):
        """
        Create Object and set to start position all objects
        :return:
        void
        """
        self.objects = Objects()
        self.init_subjects()
        self.objects.create_interface()
        self.objects.top_text.set_text("HI-SC:%d" % self.save_file.read_most())

    def create_player(self):
        self.objects.create_player(self.player_health)
        self.player = self.objects.player
        self.keydown_handlers = logic.get_keydown(self.player)
        self.keyup_handlers = logic.get_keyup(self.player)

    def in_game_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shooting(self.objects)
                elif event.key == pygame.K_p:
                    self.pause()
                if event.key == pygame.K_F5:
                    self.game_mode = "loose"
                else:
                    for handle in self.keydown_handlers[event.key]:
                        handle(event.key)
            elif event.type == pygame.KEYUP:
                for handle in self.keyup_handlers[event.key]:
                    handle(event.key)

    def menu_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.game_mode = "game"
                    self.create_game()

    def handle_events(self):
        while True:
            if self.game_mode == "menu":
                self.menu_handle()
            if self.game_mode == "game":
                self.in_game_handle()
                self.update_surface()
            if self.game_mode == "loose":
                self.save_file.write_most(self.objects.points)
                self.start_game()

    def pause(self):
        self.is_pause = not self.is_pause
        self.objects.pause_game()

    def game_over(self):
        time.sleep(2)
        self.start_game()

    def next_level(self):
        self.level += 1
        self.init_subjects()

    def init_subjects(self):
        self.create_player()
        self.objects.create_army(self.level)

    def draw_menu(self):
        menu_text = Interface(50, config.height // 2 + 200, 0, 0, "text", config.colors['red'], 22)
        menu_text.set_text("Press Enter to start")
        menu_text.draw(self.surface)
        menu_text = Interface(config.width // 2 - 30*4,
                              config.height // 2 - 190,
                              0, 0,
                              "text", config.colors['white'], 60)
        menu_text.set_text("SPACE")
        menu_text.draw(self.surface)
        menu_text = Interface(config.width // 2 - 105,
                              config.height // 2 - 120,
                              0, 0,
                              "text", config.colors['green'], 32)
        menu_text.set_text("INVADERS")
        menu_text.draw(self.surface)
        menu_text = Interface(config.width // 2 - 75,
                              config.height // 2 - 50,
                              0, 0,
                              "text", config.colors['white'], 16)
        menu_text.set_text("<- -> - MOVE")
        menu_text.draw(self.surface)
        menu_text = Interface(config.width // 2 - 75,
                              config.height // 2 - 30,
                              0, 0,
                              "text", config.colors['white'], 16)
        menu_text.set_text("SPACE - FIRE")
        menu_text.draw(self.surface)
        menu_text = Interface(config.width // 2 - 55,
                              config.height // 2 - 10,
                              0, 0,
                              "text", config.colors['white'], 16)
        menu_text.set_text("P - PAUSE")
        menu_text.draw(self.surface)
        menu_text = Interface(config.width // 2 - 75,
                              config.height // 2 + 10,
                              0, 0,
                              "text", config.colors['white'], 16)
        menu_text.set_text("F5 - restart")
        menu_text.draw(self.surface)

        self.surface.blit(textures.texture_dict[10], (config.width // 2 - 90, config.height // 2 + 55))
        menu_text = Interface(config.width // 2 - 40,
                              config.height // 2 + 55,
                              0, 0,
                              "text", config.colors['light-blue'], 16)
        menu_text.set_text("- 10 points")
        menu_text.draw(self.surface)
        self.surface.blit(textures.texture_dict[20], (config.width // 2 - 92, config.height // 2 + 80))
        menu_text = Interface(config.width // 2 - 40,
                              config.height // 2 + 80,
                              0, 0,
                              "text", config.colors['green'], 16)
        menu_text.set_text("- 20 points")
        menu_text.draw(self.surface)
        self.surface.blit(textures.texture_dict[30], (config.width // 2 - 92, config.height // 2 + 105))
        menu_text = Interface(config.width // 2 - 40,
                              config.height // 2 + 105,
                              0, 0,
                              "text", config.colors['pink'], 16)
        menu_text.set_text("- 30 points")
        menu_text.draw(self.surface)
        self.surface.blit(textures.texture_dict[300], (config.width // 2 - 105, config.height // 2 + 130))
        menu_text = Interface(config.width // 2 - 40,
                              config.height // 2 + 130,
                              0, 0,
                              "text", config.colors['pink'], 16)
        menu_text.set_text("- 300 points")
        menu_text.draw(self.surface)

        pygame.display.update()

    def start_game(self):
        """
        Start new game
        :return:
        void
        """
        self.level = 1
        self.player_health = 4
        self.game_mode = "menu"
        self.create_window()
        self.draw_menu()
        self.handle_events()

    def update_surface(self):
        """
        one game round cycle
        :return:
        void
        """
        self.surface.fill(config.colors['black'])
        if self.player.is_dead:
            self.player_health -= 1
            self.objects.player.is_dead = False
            if self.player_health == 0:
                self.game_mode = "loose"
            time.sleep(1)
            self.create_player()
            if self.objects.army.is_win:
                self.objects.create_army(self.level)
                self.objects.score_text.set_text("SCORES:%d" %
                                                 (self.objects.start_army_strength - self.objects.army.strength))

        if self.objects.army.strength == 0:
            self.next_level()

        if not self.is_pause:
            self.objects.update()
            self.objects.delete_dead()

        self.objects.draw(self.surface)

        pygame.display.update()
        self.clock.tick(config.fps)
