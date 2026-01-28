import pygame

from TextInput import TextInput
from GameScene import GameScene;

class MenuScene():
    def __init__(this, stimuliManager, width, height):
        this.nextScene = None;
        this.stimuliManager = stimuliManager;

        this.width = width;
        this.height = height;

        this.smallMenuFont = pygame.font.Font(None, 45);

        this.textBoxes = [];
        this.textBoxes.extend(
             [
             TextInput("P#ID", this.smallMenuFont, "Participant ID: ", "PXXX", (width/2) - 60, int(height*0.41), 120, 45),
             TextInput("Rows", this.smallMenuFont, "# of Rows: ", "#", (width/2) - 60, int(height*0.48), 120, 45),
             TextInput("Cards", this.smallMenuFont, "Cards per Row: ", "#", (width/2) - 60, int(height*0.55), 120, 45)
             ]
        );

        this.largeMenuFont = pygame.font.Font(None, 150);
        this.largeButtonText = pygame.font.Font(None, 125);
        this.isHovering = False;

        this.startButton = pygame.Rect((width/2) - 250, int(height*0.70), 500, 100);

        return;

    def onEvent(this, event):
        if (event.type == pygame.MOUSEMOTION):
            this.isHovering = this.startButton.collidepoint(event.pos);

        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (this.startButton.collidepoint(event.pos)):
                participantID       = this.getTextFromID("P#ID");
                numberOfRows        = this.getTextFromID("Rows"); 
                numberOfCardsPerRow = this.getTextFromID("Cards");

                try:
                    numberOfRows = int(numberOfRows);
                    numberOfCardsPerRow = int(numberOfCardsPerRow);
                except Exception:
                    return;
            
                this.nextScene = GameScene(participantID, this.stimuliManager, this.width, this.height, numberOfRows, numberOfCardsPerRow);

            selected = False;
            for box in this.textBoxes:
                if (box.rect.collidepoint(event.pos)):
                    for others in this.textBoxes:
                        others.selected = False;
                    box.selected = True;
                    box.initialText = "";
                    selected = True;
                    break;

            if (selected == False):
                for box in this.textBoxes:
                    box.selected = False;        

        if (event.type == pygame.KEYDOWN):
            for box in this.textBoxes:
                box.onPress(event);
        
        return;

    def render(this, screen):
        for box in this.textBoxes:
            box.draw(screen);
        
        surface = this.largeMenuFont.render("Familiarity Game", True, (255, 255, 255));
        screen.blit(surface, ((this.width/2) - (surface.get_width()/2), int(this.height * 0.16)));

        darkenColor = 0;
        if (this.isHovering == True):
            darkenColor = 90;

        pygame.draw.rect(screen, pygame.Color(255, 90 - darkenColor, 90 - darkenColor), this.startButton, 0);
        surface = this.largeMenuFont.render("Start", True, (255, 255, 255));
        screen.blit(surface, (this.startButton.x + (this.startButton.width/2) - (surface.get_width()/2), this.startButton.y + 10));
        
        surface = this.smallMenuFont.render("Found " + str(len(this.stimuliManager.allStimulus)) + " stimulus images.", True, (255, 255, 255));
        screen.blit(surface, (0, this.height - surface.get_height()));

        return;

    def getTextFromID(this, ID):
        for box in this.textBoxes:
            if (box.ID == ID):
                return box.text;