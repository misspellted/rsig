## rsig: Randomized Sequential Image Generator

#### History

This project was started by wondering how long it would take to randomly generate a sequence of values. The results were displayed in a console/terminal window, but that was boring. Therefore, the next logical step was to visualize it. After playing around with only creating PNG image files (one per RGB channel), it now just displays the visualizations in a more interactive manner.

#### Usage

Launch with Python 2.x: `python rsig.py` 

The following "features" are available:
 - Pressing 'f' toggles between following the mouse cursor or randomly selecting the column that is updated.
 - Pressing 'h' pauses and resumes updating columns.
 - Pressing 'p' toggles "progressive" mode on or off.
