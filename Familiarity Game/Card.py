import pygame
import math

class Card:
    def __init__(this, filePath):
        this.flipped = False;

        this.filePath = filePath;
        this.faceImage = pygame.image.load(filePath).convert();

        this.highlighting = False;
        this.revealTime = None;

        return;

    def update(this):
        if (this.revealTime == None):
            return;

        if (pygame.time.get_ticks() - this.revealTime >= 1000):
            this.flip();
            this.revealTime = None;

    def draw(this, screen, index, xSpacing, ySpacing, cardsPerRow, margin, alternative, bothFlipped):
        row = math.floor(index / cardsPerRow);
        col = index % cardsPerRow; 
        
        imgWidth, imgHeight = alternative.get_size();
        x = int((margin + col * xSpacing) + (xSpacing - imgWidth) / 2);
        y = int((margin + row * ySpacing) + (ySpacing - imgHeight) / 2);

        this.rect = pygame.Rect(x, y, imgWidth, imgHeight);

        if (this.flipped == True and bothFlipped == False):
            pygame.draw.rect(screen, pygame.Color("Black"), this.rect, width=1);
            screen.blit(this.faceImage, (x, y));
            return;

        if (bothFlipped == True):
            green = pygame.Surface(alternative.get_size(), pygame.SRCALPHA);
            green.fill((0, 255, 0, 110));

            img = this.faceImage.copy();
            img.blit(green, (0, 0), special_flags=pygame.BLEND_RGBA_MULT);

            screen.blit(img, (x, y));
            return;


        if (this.highlighting == True):
            dark = pygame.Surface(alternative.get_size(), pygame.SRCALPHA);
            dark.fill((180, 180, 180, 255));
            img = alternative.copy();
            img.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_MULT);
            screen.blit(img, (x, y));
        else:            
            screen.blit(alternative, (x, y));

        return;
    
    def scale(this, cellWidth, cellHeight, padding):
        targetWidth = cellWidth - padding * 2;
        targetHeight = cellHeight - padding * 2;

        scale = min(targetWidth / this.faceImage.get_width(), targetHeight / this.faceImage.get_height());
        this.faceImage = pygame.transform.smoothscale(this.faceImage, (int(this.faceImage.get_width() * scale), int(this.faceImage.get_height() * scale)));

    def flip(this):
        this.flipped = not this.flipped;
        return;

    def __eq__(this, other):
        return (this.filePath == other.filePath);


