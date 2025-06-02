import pygame
pygame.init()

SCREEN_SIZE=(400,600)

Screen = pygame.display.set_mode(SCREEN_SIZE)
ClockObj = pygame.time.Clock()

pygame.display.set_caption("Chess Timer")

RED = (255,0,0)
BLUE = (0,0,255)

GREY = (195,195,195)

Opponent1_color = RED
Opponent2_color = BLUE

Opponent1_millis = 27 * 60 * 1000
Opponent2_millis = Opponent1_millis

timer_event = pygame.event.custom_type()

audio_file = pygame.mixer.Sound("res/snap.wav")

opponent = 0

def drawCentredText(screen_obj: pygame.surface.Surface ,text, centre_pos, font_name, font_size, colour):
    font_obj = pygame.font.SysFont(font_name, font_size)
    text_surf = font_obj.render(text, False, colour)

    size = text_surf.get_size()

    screen_obj.blit(text_surf,[
        centre_pos[0] - (size[0]//2),
        centre_pos[1] - (size[1]//2)    
    ])

pygame.time.set_timer(timer_event, 1)

app = True

while app:
    Opponent1_in_secs = Opponent1_millis / 1000
    Opponent2_in_secs = Opponent2_millis / 1000

    Opponent1_hours = int(Opponent1_in_secs // 3600)
    Opponent2_hours = int(Opponent2_in_secs // 3600)

    Opponent1_mins = int((Opponent1_in_secs // 60) % 60)
    Opponent2_mins = int((Opponent2_in_secs // 60) % 60)

    Opponent1_secs = int(Opponent1_in_secs % 60)
    Opponent2_secs = int(Opponent2_in_secs % 60)

    if Opponent1_mins < 10:
        Opponent1_mins =  f"0{Opponent1_mins}"
    if Opponent2_mins < 10:
        Opponent2_mins =  f"0{Opponent2_mins}"

    if Opponent1_secs < 10:
        Opponent1_secs =  f"0{Opponent1_secs}"
    if Opponent2_secs < 10:
        Opponent2_secs =  f"0{Opponent2_secs}"
    

    Opponent1_text = f"{Opponent1_hours}:{Opponent1_mins}:{Opponent1_secs}" 
    Opponent2_text = f"{Opponent2_hours}:{Opponent2_mins}:{Opponent2_secs}" 


    pygame.draw.rect(Screen,Opponent1_color,(0,0,400,300))
    pygame.draw.rect(Screen,Opponent2_color,(0,300,400,300))

    drawCentredText(Screen, str(Opponent1_text), (200,150),"bankgothic",50,(255,255,255))
    drawCentredText(Screen, str(Opponent2_text), (200,450),"bankgothic",50,(255,255,255))

    drawCentredText(Screen, "Press Enter to switch",(200,300),"calibri",30,(25,25,25))

    pygame.display.update()
    ClockObj.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                audio_file.play()

                if opponent == 0:
                    opponent = 1
                else:
                    opponent = 3 - opponent

        if event.type == timer_event:

            if opponent == 1:
                Opponent1_millis -= 1

                Opponent1_color = RED
                Opponent2_color = GREY
            if opponent == 2:
                Opponent2_millis -= 1

                Opponent1_color = GREY
                Opponent2_color = BLUE


    

pygame.quit()
quit()
