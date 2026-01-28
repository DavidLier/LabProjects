import pygame
import math
import random

from Card import Card
from CardSet import CardSet
from EndScene import EndScene

class GameScene():
    def __init__(this, participantID, stimuliManager, width, height, rows, cardsPerRow):
        this.nextScene = None;

        this.participantID = participantID;
        this.stimuliManager = stimuliManager;

        this.width = width;
        this.height = height;

        this.rows = rows;
        this.cardsPerRow = cardsPerRow;

        this.stimuliManager.saveStimulusLists(participantID);

        stimulus = stimuliManager.gameStimulus;
        this.cardsPerRound = this.rows * this.cardsPerRow;

        numberOfRounds = math.ceil(len(stimulus) / (this.cardsPerRound / 2));
        print(numberOfRounds);

        this.margin = 15;

        imgWidth = (this.width - 2 * this.margin) / this.cardsPerRow;
        imgHeight = (this.height - 2 * this.margin) / this.rows;

        this.remainingCards = [];
        for s in stimulus:
            card = Card(s);
            card.scale(imgWidth, imgHeight, 10); # 10 is padding between images for the scaling
            this.remainingCards.append(card);
        
        this.alternative = pygame.image.load("back.png").convert();
        this.alternative = pygame.transform.smoothscale(this.alternative, this.remainingCards[0].faceImage.get_size());
        
        this.updateDisplayedCardSets();

        return;

    def onEvent(this, event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (len(this.getFlippedCards()) == 2):
                return;

            for pair in this.currentCardSets:
                if (pair.bothFlipped()):
                    continue;

                for card in (pair.cardOne, pair.cardTwo):
                    if (hasattr(card, "rect") == False):
                        continue;
                    if (card.rect.collidepoint(event.pos)):
                        card.flip();
        
        if (event.type == pygame.MOUSEMOTION):
            for pair in this.currentCardSets:
                for card in (pair.cardOne, pair.cardTwo):
                    if (hasattr(card, "rect") == False):
                        continue;
                    card.highlighting = (card.rect.collidepoint(event.pos));

        return;

    def render(this, screen):
        screen.fill((50, 50, 50));

        xSpacing = (this.width - 2 * this.margin) / this.cardsPerRow;
        ySpacing = (this.height - 2 * this.margin) / this.rows;

        for pair in this.currentCardSets:
            pair.update();
            pair.draw(screen, xSpacing, ySpacing, this.cardsPerRow, this.margin, this.alternative);
        
        pygame.draw.rect(screen, pygame.Color(30, 30, 30, 255), pygame.Rect(0, 0, this.width, this.height), width=10);

        for pair in this.currentCardSets:
            if (pair.active == False):
                this.currentCardSets.remove(pair);
        
        if (len(this.currentCardSets) == 0):
            this.updateDisplayedCardSets();
        
        flippedCards = this.getFlippedCards();
        if (len(flippedCards) == 2):
            if (flippedCards[0] != flippedCards[1]):
                for card in flippedCards:
                    if (card.revealTime == None):
                        card.revealTime = pygame.time.get_ticks();
        
        return;

    def updateDisplayedCardSets(this):
        this.currentCards = this.remainingCards[:int(this.cardsPerRound/2)];
        this.remainingCards = this.remainingCards[int(this.cardsPerRound/2):];

        if (len(this.remainingCards) <= 0):
            this.nextScene = EndScene(this.width, this.height);
            return;

        availableIndices = list(range(this.cardsPerRound));

        this.currentCardSets = [];
        for card in this.currentCards:
            firstIndex = random.choice(availableIndices);
            availableIndices.remove(firstIndex);

            secondIndex = random.choice(availableIndices);
            availableIndices.remove(secondIndex);

            this.currentCardSets.append(CardSet(card, firstIndex, secondIndex));
        return;

    def getFlippedCards(this):
        flippedCards = [];

        for pair in this.currentCardSets:
            for card in (pair.cardOne, pair.cardTwo):
                if (card.flipped == True):
                    flippedCards.append(card);

        return flippedCards;
