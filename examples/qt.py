# Example of embedding CEF Python browser using PyQt/PySide libraries.
# This example has two widgets: a navigation bar and a browser.
#
# Tested configurations:
# - PyQt 4.11.4 (4.8.7) on Windows
# - PySide 1.2.4 (4.8.7) on Windows
# - PyQt 4.10.4 (4.8.6) on Linux
# - PySide 1.2.1 (4.8.6) on Linux
# - CEF Python v55.4+

from cefpython3 import cefpython as cef
import ctypes
import os
import platform
import sys

# PyQt imports
if "pyqt" in sys.argv:
    # noinspection PyUnresolvedReferences
    from PyQt4.QtGui import *
    # noinspection PyUnresolvedReferences
    from PyQt4.QtCore import *
# PySide imports
elif "pyside" in sys.argv:
    # noinspection PyUnresolvedReferences
    import PySide
    # noinspection PyUnresolvedReferences
    from PySide import QtCore
    # noinspection PyUnresolvedReferences
    from PySide.QtGui import *
    # noinspection PyUnresolvedReferences
    from PySide.QtCore import *
else:
    print("USAGE:")
    print("  qt.py pyqt")
    print("  qt.py pyside")
    sys.exit(1)

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Configuration
WIDTH = 800
HEIGHT = 600

# OS differences
CefWidgetParent = QWidget
if LINUX:
    # noinspection PyUnresolvedReferences
    CefWidgetParent = QX11EmbedContainer


def main():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    app = CefApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
    app.stopTimer()
    del main_window  # Just to be safe, see below
    del app  # Must destroy before calling Shutdown
    cef.Shutdown()


def check_versions():
    print("[qt.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[qt.py] Python {ver}".format(ver=sys.version[:6]))
    # PyQt version
    if "pyqt" in sys.argv:
        # noinspection PyUnresolvedReferences
        print("[qt.py] PyQt {v1} ({v2})".format(
              v1=PYQT_VERSION_STR, v2=qVersion()))
    # PySide version
    elif "pyside" in sys.argv:
        print("[qt.py] PySide {v1} ({v2})".format(
              v1=PySide.__version__, v2=QtCore.__version__))
    # CEF Python version requirement
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.cef_widget = None
        self.navigation_bar = None
        if "pyqt" in sys.argv:
            self.setWindowTitle("PyQt example")
        elif "pyside" in sys.argv:
            self.setWindowTitle("PySide example")
        self.setFocusPolicy(Qt.StrongFocus)
        self.setupLayout()

    def setupLayout(self):
        self.resize(WIDTH, HEIGHT)
        self.cef_widget = CefWidget(self)
        self.navigation_bar = NavigationBar(self.cef_widget)
        layout = QGridLayout()
        layout.addWidget(self.navigation_bar, 0, 0)
        layout.addWidget(self.cef_widget, 1, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        frame = QFrame()
        frame.setLayout(layout)
        self.setCentralWidget(frame)
        # Browser can be embedded only after layout was set up
        self.cef_widget.embedBrowser()

    def focusInEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        # print("[qt.py] focusInEvent")
        if self.cef_widget.browser:
            if WINDOWS:
                WindowUtils.OnSetFocus(self.cef_widget.getHandle(),
                                       0, 0, 0)
            self.cef_widget.browser.SetFocus(True)

    def focusOutEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        # print("[qt.py] focusOutEvent")
        pass

    def closeEvent(self, event):
        # Close browser (force=True) and free CEF reference
        if self.cef_widget.browser:
            self.cef_widget.browser.CloseBrowser(True)
            self.cef_widget.browser = None  # free ref


class NavigationBar(QFrame):

    def __init__(self, cef_widget):
        super(NavigationBar, self).__init__()
        self.cef_widget = cef_widget

        # Init layout
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Back button
        self.back = self.createButton("back")
        # noinspection PyUnresolvedReferences
        self.back.clicked.connect(self.onBack)
        layout.addWidget(self.back, 0, 0)

        # Forward button
        self.forward = self.createButton("forward")
        # noinspection PyUnresolvedReferences
        self.forward.clicked.connect(self.onForward)
        layout.addWidget(self.forward, 0, 1)

        # Reload button
        self.reload = self.createButton("reload")
        # noinspection PyUnresolvedReferences
        self.reload.clicked.connect(self.onReload)
        layout.addWidget(self.reload, 0, 2)

        # Url input
        self.url = QLineEdit("")
        # noinspection PyUnresolvedReferences
        self.url.returnPressed.connect(self.onGoUrl)
        layout.addWidget(self.url, 0, 3)

        # Layout
        self.setLayout(layout)
        self.updateState()

    def onBack(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.GoBack()

    def onForward(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.GoForward()

    def onReload(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.Reload()

    def onGoUrl(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.LoadUrl(self.url.text())

    def updateState(self):
        browser = self.cef_widget.browser
        if not browser:
            self.back.setEnabled(False)
            self.forward.setEnabled(False)
            self.reload.setEnabled(False)
            self.url.setEnabled(False)
            return
        self.back.setEnabled(browser.CanGoBack())
        self.forward.setEnabled(browser.CanGoForward())
        self.reload.setEnabled(True)
        self.url.setEnabled(True)
        self.url.setText(browser.GetUrl())

    def createButton(self, name):
        resources = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 "resources")
        pixmap = QPixmap(os.path.join(resources, "{0}.png".format(name)))
        icon = QIcon(pixmap)
        button = QPushButton()
        button.setIcon(icon)
        button.setIconSize(pixmap.rect().size())
        return button


class CefWidget(CefWidgetParent):

    def __init__(self, parent=None):
        super(CefWidget, self).__init__(parent)
        self.parent = parent
        self.browser = None
        self.show()

    def embedBrowser(self):
        self.width = 0
        self.height = 0
        window_info = cef.WindowInfo()
        window_info.SetAsChild(self.getHandle())
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="https://www.google.com/")
        self.browser.SetClientHandler(LoadHandler(self.parent.navigation_bar))
        self.browser.SetClientHandler(FocusHandler())

    def getHandle(self):
        # PySide bug: QWidget.winId() returns <PyCObject object at 0x02FD8788>
        # There is no easy way to convert it to int.
        try:
            return int(self.winId())
        except:
            if sys.version_info[0] == 2:
                # Python 2
                ctypes.pythonapi.PyCObject_AsVoidPtr.restype = (
                        ctypes.c_void_p)
                ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = (
                        [ctypes.py_object])
                return ctypes.pythonapi.PyCObject_AsVoidPtr(self.winId())
            else:
                # Python 3
                ctypes.pythonapi.PyCapsule_GetPointer.restype = (
                        ctypes.c_void_p)
                ctypes.pythonapi.PyCapsule_GetPointer.argtypes = (
                        [ctypes.py_object])
                return ctypes.pythonapi.PyCapsule_GetPointer(
                        self.winId(), None)

    def moveEvent(self, _):
        # pos = event.pos()
        # self.x = pos.x()
        # self.y = pos.y()
        self.x = 0
        self.y = 0
        if self.browser:
            if WINDOWS:
                WindowUtils.OnSize(self.getHandle(), 0, 0, 0)
            elif LINUX:
                self.browser.SetBounds(self.x, self.y,
                                       self.width, self.height)
            self.browser.NotifyMoveOrResizeStarted()

    def resizeEvent(self, event):
        size = event.size()
        self.width = size.width()
        self.height = size.height()
        if self.browser:
            if WINDOWS:
                WindowUtils.OnSize(self.getHandle(), 0, 0, 0)
            elif LINUX:
                self.browser.SetBounds(self.x, self.y,
                                       self.width, self.height)
            self.browser.NotifyMoveOrResizeStarted()


class CefApplication(QApplication):

    def __init__(self, args):
        super(CefApplication, self).__init__(args)
        self.timer = self.createTimer()
        self.setupIcon()

    def createTimer(self):
        timer = QTimer()
        # noinspection PyUnresolvedReferences
        timer.timeout.connect(self.onTimer)
        timer.start(10)
        return timer

    def onTimer(self):
        # For best performance, a proper way of doing message loop should
        # probably be:
        #   1. In createTimer() call self.timer.start(0)
        #   2. In onTimer() call MessageLoopWork() only when
        #      QtGui.QApplication.instance()->hasPendingEvents() returns False.
        # But... there is a bug in Qt, hasPendingEvents() always returns true.
        # TODO: The bug above was noticed in Qt 4.8 on Windows. Other versions
        #       and/or other OSes may not be affected, so check it.
        cef.MessageLoopWork()

    def stopTimer(self):
        # Stop the timer after Qt's message loop has ended
        self.timer.stop()

    def setupIcon(self):
        icon_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 "resources", "{0}.png".format(sys.argv[1]))
        if os.path.exists(icon_file):
            self.setWindowIcon(QIcon(icon_file))


class LoadHandler(object):

    def __init__(self, navigation_bar):
        self.initial_app_loading = True
        self.navigation_bar = navigation_bar

    def OnLoadingStateChange(self, **_):
        self.navigation_bar.updateState()

    def OnLoadStart(self, browser, **_):
        self.navigation_bar.url.setText(browser.GetUrl())
        if self.initial_app_loading:
            # Temporary fix no. 2 for focus issue during initial loading
            # on Linux (Issue #284). If this is not applied then
            # sometimes during initial loading, keyboard focus may
            # break and it is not possible to type anything, even
            # though a type cursor blinks in web view.
            if LINUX:
                print("[qt.py] LoadHandler.OnLoadStart:"
                      " keyboard focus fix no. 2 (#284)")
                browser.SetFocus(True)
            self.initial_app_loading = False


class FocusHandler(object):

    def __init__(self):
        pass

    def OnTakeFocus(self, **kwargs):
        # print("[qt.py] FocusHandler.OnTakeFocus, next={next}"
        #       .format(next=kwargs["next_component"]]))
        pass

    def OnSetFocus(self, **kwargs):
        # source_enum = {cef.FOCUS_SOURCE_NAVIGATION: "navigation",
        #                cef.FOCUS_SOURCE_SYSTEM:     "system"}
        # print("[qt.py] FocusHandler.OnSetFocus, source={source}"
        #       .format(source=source_enum[kwargs["source"]]))
        # return False
        pass

    def OnGotFocus(self, browser, **_):
        # Temporary fix no. 1 for focus issues on Linux (Issue #284).
        # If this is not applied then when switching to another
        # window (alt+tab) and then back to this example, keyboard
        # focus becomes broken, you can't type anything, even
        # though a type cursor blinks in web view.
        if LINUX:
            print("[qt.py] FocusHandler.OnGotFocus:"
                  " keyboard focus fix no. 1 (#284)")
            browser.SetFocus(True)


if __name__ == '__main__':
    main()
