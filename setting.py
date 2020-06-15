#! /usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

class Settings():

	def __init__(self):
		'''Инициализирует статистические настройки игры'''

		#Параметры экрана
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (8, 15, 56)

		#Настройки корабля

		self.ship_limit = 3

		#Параметры пули

		self.bullet_width = 4
		self.bullet_height = 30
		self.bullet_color = randint(0, 255), randint(0, 255), randint(0, 255)
		self.bullets_allowed = 3

		#Параметры пришельцев

		self.fleet_drop_speed = 20



		#Параметры звезд
		self.star_speed = 1

		#Тем ускорения игры
		self.speedup_scale = 1.1

		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		'''Настройки изменяющиеся в ходе игры'''
		self.ship_speed_factor = 1.3
		self.bullet_speed_factor = 2
		self.alien_speed_factor = 0.5

		#Подсчет очков
		self.alien_points = 10

		#1 - вправо, -1 - влево
		self.fleet_direction = 1

	def increase_speed(self):
		'''Увеличивает настройки скорости'''
		if self.ship_speed_factor < 2:
			self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.bullets_allowed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
