import sys, random
import pygame
from  pygame.locals import *
import pygame_gui
from config import Configuration
pygame.init()
pygame.display.set_caption("Press ESC to quit")

width, height = 800, 600
window_surface = pygame.display.set_mode((width, height))
background = pygame.Surface((width, height))
background.fill(pygame.Color('#000000'))
manager = pygame_gui.UIManager((width, height))
clock = pygame.time.Clock()
is_running = True
debug = False

panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0),(width,height)), starting_layer_height=1, manager=manager)

pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1, 1), (120, 20)),text='Armature',manager=manager, container=panel)
pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1+121, 1), (25, 20)),text='Min',manager=manager, container=panel)
pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1+160, 1), (25, 20)),text='Max',manager=manager, container=panel)
pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1+199, 1), (70, 20)),text='Position',manager=manager, container=panel)
def update_data():
    global panel
    x=1
    y=21
    for key in Configuration.keys():
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x, y), (120, 20)),text=key,manager=manager, container=panel)
        if Configuration[key]['type'] == 'RoboPandaServo':
            pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x+121, y), (25, 20)),text=str(Configuration[key]['min']),manager=manager, container=panel)
            pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x+160, y), (25, 20)),text=str(Configuration[key]['max']),manager=manager, container=panel)
            pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x+199, y), (70, 20)),text=str(random.randint(0,100)),manager=manager, container=panel)
        y+=21


while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
            elif event.key == pygame.KMOD_LCTRL | K_d:
                debug = not debug # flip the value of debug (True/False)
                manager.set_visual_debug_mode(debug)

        if event.type == pygame.USEREVENT:
             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                 if event.ui_element == hello_button:
                     print('Hello World!')

        manager.process_events(event)

    update_data()

    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()