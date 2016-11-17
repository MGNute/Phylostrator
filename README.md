# The Phylostrator
A library and GUI for drawing and annotation large phylogenies, with a python application layer that can be used for scripting. 

*Dependencies*
- wxPython
- DendroPy
- PyCairo

*Programs*
- Alignment Viewer (alignment_viewer.py): A simple, lightweight application for generating graphics of multiple sequence aligmnents (nucleotides only right now) with a Phylogeny to one side and labels to the other. 
- Phylostrator (rungui.py): A dense application designed to draw phylogenies and annotate them flexibly. Functionality is particularly built in for drawing circles at certain nodes according to an annotation in a separate file, as well as for adding branches from a phylogenetic placement to the graphic.
- PNG Viewer (png_viewer.py): a lightweight GUI app that dispalys a PNG saved on disk and checks once per second to see if it has changed, and refreshes it if so.

This is a development version and contains many incomplete functions and has no guarantee that it will work. It's currently in the process of moving from displaying graphics based on the Wx drawing routines to the cairo graphics library, and that is not fully complete. Please contact me with any questions (nute2@illinois.edu). 
