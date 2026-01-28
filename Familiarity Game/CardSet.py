import pygame

from Card import Card

class CardSet:
    def __init__(this, card, firstIndex, secondIndex):
        this.firstIndex = firstIndex;
        this.secondIndex = secondIndex;

        this.cardOne = card;
        this.cardTwo = Card(card.filePath);
        this.cardTwo.faceImage = this.cardOne.faceImage;

        this.active = True;
        this.revealTime = None;

        return;

    def draw(this, screen, xSpacing, ySpacing, cardsPerRow, margin, alternative):
        this.cardOne.draw(screen, this.firstIndex, xSpacing, ySpacing, cardsPerRow, margin, alternative, (this.bothFlipped() and pygame.time.get_ticks() - this.revealTime >= 500));
        this.cardTwo.draw(screen, this.secondIndex, xSpacing, ySpacing, cardsPerRow, margin, alternative, (this.bothFlipped() and pygame.time.get_ticks() - this.revealTime >= 500));
        return;

    def update(this):
        this.cardOne.update();
        this.cardTwo.update();

        if (this.bothFlipped() == True):
            if (this.revealTime == None):
                this.revealTime = pygame.time.get_ticks();
                return;

            if (pygame.time.get_ticks() - this.revealTime >= 750):
                this.active = False;
    
    def bothFlipped(this):
        return (this.cardOne.flipped and this.cardTwo.flipped);
    
