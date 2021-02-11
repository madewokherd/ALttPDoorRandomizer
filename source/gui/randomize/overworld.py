from tkinter import ttk, Frame, Label, E, W, LEFT, RIGHT
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
    self.frames["widgets"] = Frame(self)
    self.frames["widgets"].pack(anchor=W)
    with open(os.path.join("resources","app","gui","randomize","overworld","widgets.json")) as overworldWidgets:
        myDict = json.load(overworldWidgets)
        myDict = myDict["widgets"]
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["widgets"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    return self
