import pygame
pygame.init()

import math

from variables import *


class ChessTimer(object):
    def __init__(self,time_duration: int, screen: pygame.surface.Surface, mixer: pygame.mixer.Sound):
        self.time_duration = time_duration  #time is in milliseconds

        self.screen = screen
        self.width, self.height = screen.get_size()

        self.mixer = mixer

        self.opponent1_rect = pygame.Rect(0,0,self.width//2,self.height)
        self.opponent2_rect = pygame.Rect(self.width//2,0,self.width//2,self.height)

        self.opponent1_time = self.opponent2_time = self.time_duration

        self.current_opponent = 0

        self.opponent1_color = RED
        self.opponent2_color = BLUE

        self.idle_colour = GREY

        self.opponent1_display_color = self.opponent1_color
        self.opponent2_display_color = self.opponent2_color

        self.counter_event = pygame.event.custom_type()
        pygame.time.set_timer(self.counter_event, 1)

    def initialize_time(self):
        self.opponent1_time = self.time_duration
        self.opponent2_time = self.time_duration
        self.current_opponent = 0

        self.opponent1_display_color = self.opponent1_color
        self.opponent2_display_color = self.opponent2_color


    def get_time_from_millis(self, time_millis):
        time_seconds = time_millis / 1000
        
        hrs = int(time_seconds // 3600)
        mins = int((time_seconds // 60) % 60)
        secs = int(time_seconds % 60)
        millis = int(time_millis % 1000)

        if mins < 10:
            mins =  f"0{mins}"
        if secs < 10:
            secs =  f"0{secs}"
        if len(str(millis)) == 1:
            millis = f"00{millis}"
        elif len(str(millis)) == 2:
            millis = f"0{millis}"
        
        return f"{hrs}:{mins}:{secs}.{millis}" 


    def play_function(self):
        "To put in 'while app:' loop."
        
        self.width, self.height = self.screen.get_size()
        
        self.opponent1_rect = pygame.Rect(0,0,self.width//2,self.height)
        self.opponent2_rect = pygame.Rect(self.width//2,0,self.width//2,self.height)

        timer1_ratio = self.opponent1_time / self.time_duration
        timer2_ratio = self.opponent2_time / self.time_duration

        timer1_angle = timer1_ratio * math.pi * 2
        timer2_angle = timer2_ratio * math.pi * 2

        timer1_startcircle = 0
        timer1_stopcircle = 0

        timer2_startcircle = 0
        timer2_stopcircle = 0


        pygame.draw.rect(self.screen,self.opponent1_display_color,self.opponent1_rect)
        pygame.draw.rect(self.screen,self.opponent2_display_color,self.opponent2_rect)

        drawCentredTextConstraintedWidth(self.screen, self.get_time_from_millis(self.opponent1_time), (self.width*0.25,self.height-(self.height//8)),default_font_name,self.height//8,(255,255,255),self.width//5)
        drawCentredTextConstraintedWidth(self.screen, self.get_time_from_millis(self.opponent2_time), (self.width*0.75,self.height-(self.height//8)),default_font_name,self.height//8,(255,255,255),self.width//5)

        if timer1_angle > 0:
            pygame.draw.arc(self.screen, WHITE, [self.width//4-(self.width//8),self.height//2-(self.width//8),self.width//4,self.width//4], math.pi*0.5, math.pi*0.5 + timer1_angle, 5)
        if timer2_angle > 0:
            pygame.draw.arc(self.screen, WHITE, [self.width*3//4-(self.width//8),self.height//2-(self.width//8),self.width//4,self.width//4], math.pi*0.5, math.pi*0.5 + timer2_angle, 5)

        drawResizedImgByW(self.screen,"res/pause_icon.png",[self.width//4,self.height//2],self.width//8)
        drawResizedImgByW(self.screen,"res/pause_icon.png",[self.width*3//4,self.height//2],self.width//8)

        drawCentredTextConstraintedWidth(self.screen, "Player 1", (self.width//4,self.height//8),default_font_name,self.height//8,(255,255,255),self.width//5)
        drawCentredTextConstraintedWidth(self.screen, "Player 2", (self.width*3//4,self.height//8),default_font_name,self.height//8,(255,255,255),self.width//5)
        

    def event_listener(self, event: pygame.event.Event):
    
        if event.type == pygame.KEYDOWN:

            if event.unicode in left_unicodes and self.current_opponent == 1:
                self.change_opponent()
            elif event.unicode in right_unicodes and self.current_opponent == 2:
                self.change_opponent()
            elif event.key == pygame.K_RETURN:
                self.change_opponent()

        if event.type == self.counter_event:
            if self.current_opponent == 1:
                self.opponent1_time -= 1

                self.opponent1_display_color = self.opponent1_color
                self.opponent2_display_color = self.idle_colour

            if self.current_opponent == 2:
                self.opponent2_time -= 1

                self.opponent1_display_color = self.idle_colour
                self.opponent2_display_color = self.opponent2_color

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.opponent1_rect.collidepoint(mouse_pos) and self.current_opponent == 1:
                self.change_opponent()
            if self.opponent2_rect.collidepoint(mouse_pos) and self.current_opponent == 2:
                self.change_opponent()

            if self.current_opponent == 0:
                if self.opponent1_rect.collidepoint(mouse_pos):
                    self.current_opponent = 1
                    self.mixer.play()

                if self.opponent2_rect.collidepoint(mouse_pos):
                    self.current_opponent = 2
                    self.mixer.play()


    def game_over_display(self,loser_no):
        self.width, self.height = self.screen.get_size()

        self.opponent1_rect = pygame.Rect(0,0,self.width//2,self.height)
        self.opponent2_rect = pygame.Rect(self.width//2,0,self.width//2,self.height)

        if loser_no == 1:
            text_1 = "You lost!"
            text_2 = "You won!"
        elif loser_no == 2:
            text_1 = "You won!"
            text_2 = "You lost!"

        pygame.draw.rect(self.screen,self.opponent1_color,self.opponent1_rect)
        pygame.draw.rect(self.screen,self.opponent2_color,self.opponent2_rect)

        drawCentredTextConstraintedWidth(self.screen, text_1, (self.width//2, self.height//2),default_font_name,self.height//10,(255,255,255),(self.width*1.5//2))
        drawCentredTextConstraintedWidth(self.screen, text_2, (self.width, self.height//2),default_font_name,self.height//10,(255,255,255),(self.width*1.5//2))


    def change_opponent(self):

        if self.current_opponent in {1,2}:
            self.current_opponent = 3 - self.current_opponent
        
        self.mixer.play()
