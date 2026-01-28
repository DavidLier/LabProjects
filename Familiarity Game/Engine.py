import pygame
from FamiliarityGame import FamiliarityGame

pygame.init();
pygame.display.set_caption("Familiarity Game");
pygame.display.set_icon(pygame.image.load("back.png"));

screen = pygame.display.set_mode(size=(1280, 720), display=0);
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=0);

width, height = screen.get_size();
game = FamiliarityGame(width, height);

clock = pygame.time.Clock();

while game.running:
    screen.fill((0, 0, 0));

    for event in pygame.event.get():
        game.onEvent(event);
    
    game.render(screen);
    pygame.display.flip();

    clock.tick(60);

pygame.quit();