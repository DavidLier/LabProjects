package me.david.paradgim;

import lombok.Getter;
import lombok.Setter;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class Event {

    @Getter private final int eventTime;
    @Getter private final int eventDuration;

    @Getter private BufferedImage toDisplay;

    @Getter @Setter private boolean active;

    public Event(int eventTime, int eventDuration, File image) {
        this.eventTime = eventTime;
        this.eventDuration = eventDuration;

        try {
            toDisplay = ImageIO.read(image);
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("UNABLE TO LOAD IMAGE:" + image.getAbsolutePath());
        }
    }
}
