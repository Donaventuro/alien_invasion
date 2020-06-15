#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

	def __init__(self, ai_settings, screen):
		'''Инициализирует корабль и задает начальную позицию'''
		super(Ship, self).__init__()

		self.screen = screen
		self.ai_settings = ai_settings



		#Загрузка изображения корабля и получение прямоугольника

		self.image = pygame.image.load('images/ship.gif')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		#Каждый новый корабль появляется у нижнего края экрана

		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		self.center = float(self.rect.centerx)

		#флаг перемещения
		self.moving_right = False
		self.moving_left = False




	def update(self):
		'''Обновляет позицию корабля с учатом флага'''
		if (self.moving_right and
			self.rect.right < self.screen_rect.right):
			self.image = pygame.image.load('images/ship3.gif')
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
			self.image = pygame.image.load('images/ship2.gif')

		elif (not self.moving_left) and (not self.moving_right):
				self.image = pygame.image.load('images/ship.gif')

		self.rect.centerx = self.center



	def blitme(self):
		'''Рисует корабль в текущей позиции'''
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		self.center = self.screen_rect.centerx
