import pygame
from math import floor

SCREEN_SIZE = (800,400)
FPS = 60

default_font_name = "bankgothic"

click_sound = "res/snap.wav"

icon_paths = {
    "pause": "res/pause_icon.png",
    "retry":"res/retry.png",
    "clock": "res/clock_button.png",


    "escape": "res/escape_button.png",
    "confirm":"res/yes_button.png",
    
    "up": "res/up_arrow.png",
    "down":"res/down_arrow.png"

}

RED = (205, 0, 0)
BLUE = (0, 0, 205)

GREY = (195, 195, 195)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

left_keyids = {pygame.K_q,pygame.K_w,pygame.K_e,pygame.K_r,pygame.K_t,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_f,pygame.K_z,pygame.K_x,pygame.K_c,pygame.K_v}
right_keyids = {pygame.K_y,pygame.K_u,pygame.K_i,pygame.K_o,pygame.K_p,pygame.K_g,pygame.K_h,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_b,pygame.K_n,pygame.K_m}

left_unicodes = "qwetasdfzxc\r"
right_unicodes = "uiopjklnm\r"

def drawCentredText(screen_obj: pygame.surface.Surface ,text, centre_pos, font_name, font_size, colour):
    font_obj = pygame.font.SysFont(font_name, font_size)
    text_surf = font_obj.render(text, False, colour)

    size = text_surf.get_size()

    screen_obj.blit(text_surf,[
        centre_pos[0] - (size[0]//2),
        centre_pos[1] - (size[1]//2)    
    ])

    return pygame.Rect(
        centre_pos[0] - (size[0]//2),
        centre_pos[1] - (size[1]//2),
        size[0],
        size[1]
    )

def drawCentredTextConstraintedWidth(screen_obj: pygame.surface.Surface ,text, centre_pos, font_name, font_size, colour, max_width: int):
    original_text_surf = pygame.font.SysFont(font_name, font_size).render(text, False, colour)

    if original_text_surf.get_width() > max_width:
        orig_width = original_text_surf.get_width()
        new_font_size = floor(original_text_surf.get_height() * max_width // orig_width)
        text_surf = pygame.transform.scale(original_text_surf, [max_width, new_font_size])
        
        screen_obj.blit(text_surf,
                        [centre_pos[0]-(text_surf.get_width()//2),
                         centre_pos[1]-(text_surf.get_height()//2)])
        
        return text_surf
    else:
        screen_obj.blit(original_text_surf,
                        [centre_pos[0]-(max_width//2),
                         centre_pos[1]-(original_text_surf.get_height()//2)])
        
        return original_text_surf
    



def drawResizedImgByW(screen_obj: pygame.surface.Surface, img_path: str, centre_pos: tuple[int], width: int):
    original_img = pygame.image.load(img_path)

    old_img_size = original_img.get_size()

    new_height =  width * old_img_size[1] / old_img_size[0] 

    new_img = pygame.transform.scale(original_img, [width, new_height])

    screen_obj.blit(new_img,
                    [
                        centre_pos[0] - (width // 2),
                        centre_pos[1] - (new_height // 2)
                    ]
    )

    return pygame.Rect(
        centre_pos[0] - (width // 2),
        centre_pos[1] - (new_height // 2),
        width,
        new_height
    )