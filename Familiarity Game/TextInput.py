import pygame

class TextInput:
    def __init__(this, ID, font, preLabel, initialText, x, y, width, height):
        this.ID = ID;
        this.font = font;
        this.preLabel = preLabel;
        this.initialText = initialText;
        this.rect = pygame.Rect(x, y, width, height);
    
        this.selected = False;
        this.text = "";

    def draw(this, screen):
        color = pygame.Color("White");
        if (this.selected == True):
            color = pygame.Color("Red");

        textToRender = this.text;
        if (len(this.initialText) > 0):
            textToRender = this.initialText;
        
        surface = this.font.render(textToRender, True, (255, 255, 255));
        screen.blit(surface, (this.rect.x + 5, this.rect.y + 10));

        pygame.draw.rect(screen, color, this.rect, 3);
    
        surface = this.font.render(this.preLabel, True, (255, 255, 255));
        screen.blit(surface, (this.rect.x - surface.get_width(), this.rect.y + 10));

    def onPress(this, event):
        if (this.selected == False):
            return;
    
        if (event.key == pygame.K_RETURN):
            this.selected = False;
            return;

        if (event.key == pygame.K_BACKSPACE):
            this.text = this.text[:-1];
            return;

        this.text = this.text + event.unicode;
        this.initialText = "";

