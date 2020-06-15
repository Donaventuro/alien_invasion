import pygame
from pygame.sprite import  Group
from pygame.sprite import Sprite
from random import randint

from setting import Settings
from ship import Ship
from button import Button
from scoreboard import Scoreboard
from logo import Logo

import game_functions as gf
from game_stats import GameStats



def run_game():

	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height), 0)
	pygame.display.set_caption('Alien Invasion')
	icon = pygame.image.load('images/shipmini.gif')
	pygame.display.set_icon(icon)




	play_Button = Button(ai_settings, screen, 0, 'Play')
	quit_Button = Button(ai_settings, screen, 50, 'Quit')


	stats = GameStats(ai_settings)

	sb = Scoreboard(ai_settings, screen, stats)

	ship = Ship(ai_settings, screen)

	bullets = Group()

	logo = Logo(screen)


	stars = Group()
	gf.add_star(ai_settings, screen, stars)

	aliens = Group()
	gf.create_fleet(ai_settings, screen, ship, aliens)


	timer = pygame.time.Clock()
	while True:
			timer.tick(150)
			gf.check_events(ai_settings, screen, stats, sb, play_Button,
								quit_Button, ship, aliens, bullets)

			ai_settings.bullet_color = randint(0, 255), randint(0, 255), randint(0, 255)

			if stats.game_active:

				ship.update()

				gf.update_bullets(ai_settings, screen, stats, sb, ship,
								aliens, bullets)

				gf.update_stars(stars, screen, ai_settings)

				gf.check_bul_al_collis(ai_settings, screen, stats, sb,
										ship, aliens, bullets)


				gf.update_aliens(ai_settings, screen, stats, sb, ship,
								aliens, bullets)



			gf.update_screen(ai_settings, screen, ship, aliens,
							bullets, stars, stats, sb, play_Button,
							 quit_Button, logo)


run_game()
