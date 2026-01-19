package me.david.util;

import me.david.fNIRSParadigm;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Launcher {

    public static void main(String[] args) {
        Context currentContext = null;
        try {
            int breakBlockMin = Integer.parseInt(args[0]);
            int breakBlockMax = Integer.parseInt(args[1]);
            int taskBlockMin = Integer.parseInt(args[2]);
            int taskBlockMax = Integer.parseInt(args[3]);

            int numberOfLargeBlocks = Integer.parseInt(args[4]);
            List<String> taskBlockFoldersPaths = new ArrayList<String>();
            taskBlockFoldersPaths.addAll(Arrays.asList(args).subList(5, numberOfLargeBlocks + 5));

            currentContext = new Context(breakBlockMin, breakBlockMax, taskBlockMin, taskBlockMax, taskBlockFoldersPaths);
        } catch (Exception e) { e.printStackTrace(); }

        if (currentContext == null) {
            System.out.println("ERROR: Could not create context from given arguments.");
            return;
        }

        new fNIRSParadigm(currentContext);
    }

}
