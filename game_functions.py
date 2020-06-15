#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import sleep

from random import randint

import pygame

from bullet import Bullet
from alien import Alien
from stars import Star



def update_screen(ai_settings, screen, ship, aliens, bullets, stars,
					stats, sb,  play_Button, quit_Button, logo):
	'''Обновляет избр на экране и отображает новый экран'''

	#При каждом проходе цикла прорисовывается экран
	screen.fill(ai_settings.bg_color)

	#Позади всех элементов выстраиваются звезды
	stars.draw(screen)



	#Игра неактивна? кнопка Play!	 Активна? Запуск игры
	if not stats.game_active:

		logo.update()
		logo.blitme()
		if logo.rect.y > 70:
			play_Button.draw_button()
			quit_Button.draw_button()




	else:
		#Всё пули выводятся позади изображений корабля и пришельцев
		for bullet in bullets.sprites():
			bullet.draw_bullet()
		ship.blitme()
		aliens.draw(screen)

		#Вывод счета
		sb.show_score()



	#Отображение последнего прорисованного экрана
	pygame.display.flip()


def check_events(ai_settings, screen, stats, sb, play_Button,
					quit_Button, ship, aliens, bullets):
	'''Обрабатывает нажания клавиш и события мыши'''

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, stats, aliens,
								screen, ship, bullets, sb)

		if event.type == pygame.KEYUP:
			check_keyup_events(event, ship)

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb,
								play_Button, ship,aliens, bullets,
								mouse_x, mouse_y)
			check_quit_button(quit_Button, stats, mouse_x, mouse_y)


def check_keydown_events(event, ai_settings, stats, aliens, screen,
							ship, bullets, sb):
	'''Реагирует на нажатие клавиш'''

	if event.key == pygame.K_RIGHT:
		ship.moving_right = True


	if event.key == pygame.K_LEFT:
		ship.moving_left = True


	if event.key == pygame.K_SPACE and stats.game_active:

		fire_bullet(ai_settings, screen, ship, bullets)


	elif event.key == pygame.K_ESCAPE and not stats.game_active:
		pygame.display.quit()
		sys.exit()

	elif event.key == pygame.K_ESCAPE and stats.game_active:
		check_pause = True
		pygame.mouse.set_visible(True)
		stats.game_active = False
		aliens.empty()
		bullets.empty()

	elif event.key == pygame.K_SPACE and not stats.game_active:

		start_game(ai_settings, screen, ship, aliens, stats, sb)


def check_keyup_events(event, ship):
	'''Реагирует на отпускание клавиш'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False


	if event.key == pygame.K_LEFT:
		ship.moving_left = False





def check_play_button(ai_settings, screen, stats, sb, play_Button,
						ship, aliens, bullets, mouse_x, mouse_y):
	'''Запускает новую игру при нажатии на Play'''

	button_clicked = play_Button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:

	#Сброс игровой статистики
		stats.reset_stats()
		stats.game_active = True



		start_game(ai_settings, screen, ship, aliens, stats, sb)

def check_quit_button(quit_Button, stats, mouse_x, mouse_y):

	button_clicked = quit_Button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		pygame.display.quit()
		sys.exit()


def start_game(ai_settings, screen, ship, aliens, stats, sb):


	sb.prep_images()

	ai_settings.initialize_dynamic_settings()
	pygame.mouse.set_visible(False)
	stats.reset_stats()
	stats.game_active = True

	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship()



def fire_bullet(ai_settings, screen, ship, bullets):
	'''Выпускает пулю, если максимум еще не достигнут'''

	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)



def update_bullets(ai_settings, screen, stats, sb, ship, aliens,
					bullets):
	'''Обновляет позиции пуль и уничтожает старые пули'''

	#Обновление позиции пуль
	bullets.update()



	#Удаление пуль, вышедших за край экрана
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bul_al_collis(ai_settings, screen, stats, sb, ship, aliens,
						bullets)


def check_high_score(stats, sb):
	'''Проверяет, появился ли новый рекорд'''
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def check_bul_al_collis(ai_settings, screen, stats, sb, ship, aliens,
						bullets):
	'''Обработка коллизий пуль с пришельцами'''
	#Удаление пуль и пришельцев, учавстствующих в коллизиях
	collisions = pygame.sprite.groupcollide(bullets, aliens, True , True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
		sb.prep_score()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		#Уничтожение существующих пуль и создание нового флота
		bullets.empty()
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
	'''Вычисляет количество пришельцев в ряду'''
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int((available_space_x/(1.4*alien_width)) - 1)
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	'''Определяет количество рядов, помещающихся на экране'''
	available_space_y = (ai_settings.screen_height -
						(3*alien_height) - ship_height)

	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	'''Создает пришельца и размещает его в ряду'''

	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 1.5*alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 1.5*alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	'''Создает флот пришельцев'''
	alien = Alien(ai_settings, screen)

	#Создание пришельца и вычисление количества пришельцев в ряду
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	#Создание флота пришельцев
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
						row_number)


def check_fleet_edges(ai_settings, aliens):
	'''Реагирует на достижение края экрана'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	'''Опускает и меняет направление'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
						bullets):
	'''Проверяет, достиг ли флот низа'''

	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens,
					bullets):
	'''Обновляет пришельцев. При столкновении создает новый флот'''

	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens,
					bullets)

	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
						bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	'''Обрабатывает столкновение корябля с пришельцами'''
	#Уменьшение ship_left
	if stats.ship_left > 0:

		stats.ship_left -= 1

		#Очистка списков пришельцев и пуль
		aliens.empty()
		bullets.empty()
		sb.prep_ships()

		#Создание нового флота и размещение корабля в центре
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		#Пауза
		sleep(0.5)

	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)



def add_star(ai_settings, screen, stars):
	'''Создает звезды'''

	star = Star(screen, ai_settings)

	available_space_x = ai_settings.screen_width - 25
	number_star_x = int(available_space_x/15)

	available_space_y = ai_settings.screen_height - 25
	number_rows = int(available_space_y / 15)

	for row_number in range(12):
		for star_number in range(17):
			star = Star(screen, ai_settings)


			star.rect.x = 50 * star_number + randint(-20, 20)
			star.rect.y = 50 * row_number + randint(-20, 20)
			stars.add(star)

def update_stars(stars, screen, ai_settings):
	'''Обновляет звезды с учетом их движения'''
	stars.update(ai_settings)

	for star in stars:
		if star.check_stars():
			star.rect.y = 0
