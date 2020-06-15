#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class Logo():

	def __init__(self, screen):

		self.screen = screen



		self.image = pygame.image.load('images/logo.gif')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		#Каждый новый корабль появляется у нижнего края экрана

		self.rect.centerx = self.screen_rect.centerx - 20
		self.rect.top = self.screen_rect.top - 200
		self.y = float(self.rect.y)

	def update(self):
		if self.y < 80:
			self.y += 1
			self.rect.y = self.y



	def blitme(self):
		'''Рисует корабль в текущей позиции'''
		self.screen.blit(self.image, self.rect)
