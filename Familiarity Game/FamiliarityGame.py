import pygame

from MenuScene import MenuScene
from StimuliManager import StimuliManager

participantID = "";

class FamiliarityGame:
    def __init__(this, width, height):
        this.running = True;

        this.width = width;
        this.height = height;

        this.stimuliManager = StimuliManager();
        this.currentScene = MenuScene(this.stimuliManager, this.width, this.height);

        return;

    def onEvent(this, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_ESCAPE):
                this.running = False;
    
        if (event.type == pygame.QUIT):
            this.running = False;      
         
        this.currentScene.onEvent(event);            
        
        if not (this.currentScene.nextScene == None):
            this.currentScene = this.currentScene.nextScene;

        return;

    def render(this, screen):
        this.currentScene.render(screen);                     
        return;
