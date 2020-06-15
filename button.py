import pygame.font

class Button():

	def __init__(self, ai_settings, screen, recty, msg):

		self.screen = screen
		self.screen_rect = screen.get_rect()

		self.width, self.height = 200, 50
		self.button_color = (255, 255, 0)
		self.text_color = (255,255,0)
		self.font = pygame.font.Font('Hardpixel.ttf', 31)

		self.rect = pygame.Rect(0,0, self.width, self.height)
		self.rect.centerx = self.screen_rect.centerx
		self.rect.centery = self.screen_rect.centery + recty

		self.prep_msg(msg)



	def prep_msg(self, msg):
		self.msg_image = self.font.render(msg, True, self.text_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		
		self.screen.blit(self.msg_image, self.msg_image_rect)


