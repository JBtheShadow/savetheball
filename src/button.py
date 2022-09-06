import pygame
from globals import *

class Button:
    def __init__(self, text, func, func_param, width, height):
        self.width = width or 100
        self.height = height or 100
        self.func = func or (lambda: print((text or "No text") + " was clicked"))
        self.func_param = func_param
        self.text = text or "No text"
        self.btn_x = 0
        self.btn_y = 0
        self.text_x = 0
        self.text_y = 0

    def check_pressed(self, mouse_x, mouse_y, cursor_radius):
        if mouse_x + cursor_radius >= self.btn_x and mouse_x - cursor_radius <= self.btn_x + self.width:
            if mouse_y + cursor_radius >= self.btn_y and mouse_y - cursor_radius <= self.btn_y + self.height:
                if self.func_param is not None:
                    self.func(self.func_param)
                else:
                    self.func()
                return True
    
    def draw(self, win: pygame.Surface, btn_x, btn_y, text_x, text_y):
        self.btn_x = btn_x or self.btn_x
        self.btn_y = btn_y or self.btn_y

        if text_x:
            self.text_x = text_x + self.btn_x
        else:
            self.text_x = self.btn_x
        
        if text_y:
            self.text_y = text_y + self.btn_y
        else:
            self.text_y = self.btn_y
        
        pygame.draw.rect(win, (150, 150, 150), (self.btn_x, self.btn_y, self.width, self.height), border_radius = 5)
        btn_text = default_font.render(self.text, 1, (25, 25, 25))
        win.blit(btn_text, (self.text_x, self.text_y))
