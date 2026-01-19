package me.david.util;

import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

public class Context {
    @Getter private final int breakBlockMin;
    @Getter private final int breakBlockMax;
    @Getter private final int taskBlockMin;
    @Getter private final int taskBlockMax;

    @Getter private final List<String> taskBlockFolders = new ArrayList<String>();

    public Context(int bBMin, int bBMax, int tBMin, int tBMax, List<String> taskBlockFolders) {
        this.breakBlockMin = bBMin;
        this.breakBlockMax = bBMax;

        this.taskBlockMin = tBMin;
        this.taskBlockMax = tBMax;

        this.taskBlockFolders.addAll(taskBlockFolders);
    }
}
