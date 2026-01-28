import pygame

class EndScene():
    def __init__(this, width, height):
        this.nextScene = None;

        this.width = width;
        this.height = height;

        this.largeFont = pygame.font.Font(None, 100);

        return;

    def onEvent(this, event):                
        return;

    def render(this, screen):        
        surface = this.largeFont.render("Thank you for participating.", True, (255, 255, 255));
        screen.blit(surface, ((this.width/2) - (surface.get_width()/2), (this.height/2) - (surface.get_height()/2)));
        return;