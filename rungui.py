__author__ = 'Michael'
import gui_manager
import threading

class app_thread(threading.Thread):

    def __init__(self):
        super(app_thread,self).__init__()
        self.app=None

    def run(self):
        self.app = gui_manager.MyApp()
        self.app.MainLoop()




if __name__ == '__main__':
    app = gui_manager.MyApp()
    # top = main.gui_manager.gui_manager(None)
    # top.Show(True)
    # print(wx.GetTopLevelWindows())
    app.MainLoop()
    # print wx.GetTopLevelWindows()