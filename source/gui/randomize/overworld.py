from tkinter import ttk, Frame, Label, W, E, NW, LEFT, RIGHT, X, Y, TOP
import source.gui.widgets as widgets
import json
import os

def overworld_page(parent):
    # Overworld Shuffle
    self = ttk.Frame(parent)

    # Overworld Shuffle options
    self.widgets = {}

    # Overworld Shuffle option sections
    self.frames = {}

    # Load Overworld Shuffle option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    # These get split left & right
    self.frames["leftOverworldFrame"] = Frame(self)
    self.frames["rightOverworldFrame"] = Frame(self)
    self.frames["leftOverworldFrame"].pack(side=LEFT, anchor=NW)
    self.frames["rightOverworldFrame"].pack(anchor=NW)
    
    with open(os.path.join("resources","app","gui","randomize","overworld","widgets.json")) as overworldWidgets:
        myDict = json.load(overworldWidgets)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.widgets[key] = dictWidgets[key]
                if framename == "rightOverworldFrame":
                    self.widgets[key].pack(side=LEFT)
                else:
                    self.widgets[key].pack(anchor=E)

    return self
