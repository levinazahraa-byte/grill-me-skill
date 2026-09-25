# -*- coding: utf-8 -*-
"""Builds all five art-direction explorations of the same portfolio."""
import os, sys
import deckkit
import v01_bedazzled, v02_dollhouse, v03_softdesk, v04_aero, v05_chat

OUT = os.path.dirname(os.path.abspath(__file__))
VERSIONS = [("01", "bedazzled", v01_bedazzled), ("02", "dollhouse", v02_dollhouse),
            ("03", "softdesk", v03_softdesk), ("04", "aero", v04_aero),
            ("05", "chat", v05_chat)]

for num, name, mod in VERSIONS:
    d = deckkit.Deck()
    mod.build(d)
    path = os.path.join(OUT, "portfolio-%s-%s.pptx" % (num, name))
    d.save(path)
    print("  %s  %-10s %2d slides  %s" % (num, name, len(d.prs.slides._sldIdLst),
                                          os.path.basename(path)))
