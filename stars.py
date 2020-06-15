#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.sprite import Sprite

class Star(Sprite):
	'''Класс, представляющий одну звезду'''

	def __init__(self, screen, ai_settings):
		'''Иницилизирует звезду и задает её начальную позицию'''
		super().__init__()
		self.screen = screen

		self.image = pygame.image.load('images/star.gif')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.rect.centerx = self.screen_rect.centerx

		self.rect.centery = self.screen_rect.centery

		self.color = 30,30,30

		self.speed_factor = ai_settings.star_speed

	def update(self, ai_settings):

		self.rect.y += self.speed_factor



	def check_stars(self):

		if self.rect.bottom >= self.screen_rect.bottom:
			return True
