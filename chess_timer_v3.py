import pygame
pygame.init()

from objects import *
from variables import *

Screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE, 64)
ClockObj = pygame.time.Clock()

audio_file = pygame.mixer.Sound(click_sound)

pygame.display.set_caption("Chess Timer")


class ScreenChanger(object):
    def __init__(self, screen:pygame.surface.Surface,clock_object:pygame.time.Clock, fps: int = 60):
        self.screen = screen
        self.clock = clock_object

        self.width, self.height = self.screen.get_size()

        self.app = True

        self.fps = fps
        self.chess_timer = ChessTimer(0.05 * 60 * 1000, self.screen, audio_file)

        self.scene_id = "set_time_duration_scene"
        
        self.scenes_dict = {
            "timer_scene": lambda: self.timer_scene(),
            "end_timer_scene": lambda: self.end_timer_scene(),
            "set_time_duration_scene": lambda: self.set_time_duration_scene()
        }

        while self.app:
            if self.scene_id in self.scenes_dict.keys():
                self.current_scene = self.scenes_dict[self.scene_id]

            self.current_scene()

        pygame.quit()
        quit()


    def set_time_duration_scene(self):
        self.scene_id = "set_time_duration_scene"

        self.width, self.height = self.screen.get_size()

        hrs = 0
        mins = 0
        secs = 5

        while self.app and self.scene_id == "set_time_duration_scene":
            self.width, self.height = self.screen.get_size()
            
            pygame.draw.rect(
                self.screen, 
                pygame.Color(120,19,19),
                [self.width//8,self.height//8,self.width*3//4,self.width*3//8],
                border_radius = 20
            )
            
            hrs_txt = str(hrs)
            mins_txt = str(mins)
            secs_txt = str(secs)

            if hrs < 10:
                hrs_txt = "0" + hrs_txt
            if mins < 10:
                mins_txt = "0" + mins_txt
            if secs < 10:
                secs_txt = "0" + secs_txt
            

            drawCentredText(self.screen,str(hrs_txt),[self.width//4,self.height//2],default_font_name,self.height//4,WHITE)
            drawCentredText(self.screen,str(mins_txt),[self.width//2,self.height//2],default_font_name,self.height//4,WHITE)
            drawCentredText(self.screen,str(secs_txt),[self.width*3//4,self.height//2],default_font_name,self.height//4,WHITE)
            
            drawCentredText(self.screen,":",[self.width*3//8,self.height//2],default_font_name,75,WHITE)
            drawCentredText(self.screen,":",[self.width*5//8,self.height//2],default_font_name,75,WHITE)
            
            drawCentredText(self.screen,"Hours",[self.width//4,self.height*13//16],default_font_name,self.height//16,WHITE)
            drawCentredText(self.screen,"Minutes",[self.width//2,self.height*13//16],default_font_name,self.height//16,WHITE)
            drawCentredText(self.screen,"Seconds",[self.width*3//4,self.height*13//16],default_font_name,self.height//16,WHITE)
            
            escape = drawResizedImgByW(self.screen, icon_paths["escape"],(self.width//8,self.height//8),self.height//8)
            confirm = drawResizedImgByW(self.screen, icon_paths["confirm"],(self.width*7//8,self.height//8),self.height//8)

            hr_up = drawResizedImgByW(self.screen, icon_paths["up"],[self.width//4,self.height*5//16],self.width//16)
            min_up = drawResizedImgByW(self.screen, icon_paths["up"],[self.width//2,self.height*5//16],self.width//16)
            sec_up = drawResizedImgByW(self.screen, icon_paths["up"],[self.width*3//4,self.height*5//16],self.width//16)

            hr_down = drawResizedImgByW(self.screen, icon_paths["down"],[self.width//4,self.height*11//16],self.width//16)
            min_down = drawResizedImgByW(self.screen, icon_paths["down"],[self.width//2,self.height*11//16],self.width//16)
            sec_down = drawResizedImgByW(self.screen, icon_paths["down"],[self.width*3//4,self.height*11//16],self.width//16)

            pygame.display.update()
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if escape.collidepoint(pygame.mouse.get_pos()):
                        self.chess_timer.initialize_time()
                        self.scene_id = "timer_scene"

                    if confirm.collidepoint(pygame.mouse.get_pos()):
                        if secs != 0 or mins != 0 or hrs != 0: 
                            self.chess_timer.time_duration = 1000 * ((hrs*3600)+(mins*60)+secs)
                            self.chess_timer.initialize_time()
                            self.scene_id = "timer_scene"

                    if hr_up.collidepoint(pygame.mouse.get_pos()) and hrs < 23:
                        hrs += 1
                    if hr_down.collidepoint(pygame.mouse.get_pos()) and hrs > 0:
                        hrs -= 1
                
                    if min_up.collidepoint(pygame.mouse.get_pos()) and mins < 59:
                        mins += 1
                    if min_down.collidepoint(pygame.mouse.get_pos()) and mins > 0:
                        mins -= 1

                    if sec_up.collidepoint(pygame.mouse.get_pos()) and secs < 59:
                        secs += 1
                    if sec_down.collidepoint(pygame.mouse.get_pos()) and secs > 0:
                        secs -= 1


    def end_timer_scene(self):
        self.scene_id = "end_timer_scene"

        if self.chess_timer.opponent1_time < 0:
            loser = 1
        else:
            loser = 2

        while self.app and self.scene_id == "end_timer_scene":
            
            self.chess_timer.game_over_display(loser)

            self.width, self.height = self.screen.get_size()

            retry = drawResizedImgByW(self.screen, icon_paths["retry"],(self.width//2,self.height//4),self.height//8)
            set_timer = drawResizedImgByW(self.screen, icon_paths["clock"],(self.width//2,self.height*3//4),self.height//8)


            pygame.display.update()
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry.collidepoint(pygame.mouse.get_pos()):
                        self.chess_timer.initialize_time()
                        self.scene_id = "timer_scene"
                    if set_timer.collidepoint(pygame.mouse.get_pos()):
                        self.scene_id = "set_time_duration_scene"


    def timer_scene(self):
        self.scene_id = "timer_scene"

        while self.app and self.scene_id == "timer_scene":
            self.chess_timer.play_function()

            set_timer = drawResizedImgByW(self.screen, icon_paths["clock"],(self.width//2,self.height//2),self.height//8)

            if self.chess_timer.opponent1_time <= 0 or self.chess_timer.opponent2_time <= 0:
                self.scene_id = "end_timer_scene"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if set_timer.collidepoint(pygame.mouse.get_pos()):
                        self.scene_id = "set_time_duration_scene"


                self.chess_timer.event_listener(event)

            pygame.display.update()
            self.clock.tick(self.fps)


GameObject = ScreenChanger(Screen, ClockObj, FPS)                                                                              
