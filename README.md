"# Python For Maya" 

For creating UI's for Maya you have 2 options
    - using the Maya cmd library 
    - using Qt

 Qt
    - developed as a response to make maya's code more multiplatform 
    - Maya 2011 - 2016 -> Qt4
    - Maya 2017+ -> Qt5
    - Qt is mostly for C++ API but a company called riverbank made PyQt allowing us to use Qt within Python
        - but there's a licensing issue
    - Pyside is backed by the Qt foundation and has no licensing issues, it's pretty much the same as PyQt
    - Maya 2011 - 2016 -> Qt4, Pyside
    - Maya 2017+ -> Qt5, Pyside 2
    - It's hard to write code that works on both Qt4 and 5. There's a popular Abstraction Library called Qt.py
        - This is used by many studios
        - provides a simple layer above both Qt4 and 5 APIs, and it'll redirect any calls to the relevant API

Qt5
from Qt import QtWidgets, QtGui, QtCore
from PySide2 import QtWidgets, QtGui, QtCore
from PyQt5 import QtWidgets, QtGui, QtCore

Qt4
from Qt import QtWidgets, QtGui, QtCore
from PySide import QtGui, QtCore
from PyQt4 import QtGui, QtCore

Qt vs cmds
- cmds was built for MEL
- UI functions in cmds only represent a small subset of Qt
- cmds is much easier to learn
- cmds cannot be used outside Maya
- cmds requires you to know the UI type before modifying it
- Hard to change UI elements in cmds
- cmds down't scale as well as Qt for large projects

Ducktyping
 - "If it walks like a duck and quacks like a duck, then it's a duck"
 - for example, a string is the same thing as a list of characters
 - this allows us to make functions that don't care what the type of the parameters are. As long as they have the same interface  
 
https://github.com/mottosso/Qt.py

PyQt5 Documentation - pyqt.sourceforge.net/Docs/PyQt5
nullege.com - search PyQt5