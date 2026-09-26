# -*- coding: utf-8 -*-
"""Builds the five art directions of the Content Production portfolio."""
import os
import deckkit
import cp01_bedazzled, cp02_dollhouse, cp03_softdesk, cp04_aero, cp05_chat

OUT = os.path.dirname(os.path.abspath(__file__))
V = [("01", "bedazzled", cp01_bedazzled), ("02", "dollhouse", cp02_dollhouse),
     ("03", "softdesk", cp03_softdesk), ("04", "aero", cp04_aero),
     ("05", "chat", cp05_chat)]
for num, name, mod in V:
    d = deckkit.Deck()
    mod.build(d)
    p = os.path.join(OUT, "content-portfolio-%s-%s.pptx" % (num, name))
    d.save(p)
    print("  %s %-10s %2d slides" % (num, name, len(d.prs.slides._sldIdLst)))
