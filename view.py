__author__ = 'Michael'

from abc import ABCMeta

class AbstractView():

    def __init__(self):
        pass

class WxGUIConnectorView(AbstractView):

    def __init__(self):
        AbstractView.__init__(self)

    # TODO: fill this in with connenctions to the gui_manager

