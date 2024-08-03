import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

class SplitViewWidget(QWidget):
    def __init__(self, parent=None):
        super(SplitViewWidget, self).__init__(parent)
        self.splitter = QSplitter(Qt.Horizontal)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)
        self.splitter.setSizes([1, 1])  # Initialize sizes for the split panels

    def add_webview(self, url="https://www.google.com"):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        self.splitter.addWidget(browser)
        return browser

class AnimatedButton(QToolButton):
    def __init__(self, icon, parent=None):
        super(AnimatedButton, self).__init__(parent)
        self.setIcon(icon)
        self.setIconSize(QSize(24, 24))
        self.setStyleSheet("border: none;")
        self.animation = QPropertyAnimation(self, b"iconSize")
        self.animation.setDuration(200)
        self.enterEvent = self.startAnimation
        self.leaveEvent = self.endAnimation

    def startAnimation(self, event):
        self.animation.setEndValue(QSize(28, 28))
        self.animation.start()

    def endAnimation(self, event):
        self.animation.setEndValue(QSize(24, 24))
        self.animation.start()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.create_tab()

        self.showMaximized()

        # Navbar
        navbar = QToolBar()
        navbar.setStyleSheet("background-color: #2b2b2b;")
        self.addToolBar(navbar)

        back_btn = AnimatedButton(QIcon('icons/back.png'), self)
        back_btn.clicked.connect(self.back)
        navbar.addWidget(back_btn)
        navbar.addWidget(self.create_spacer())

        forward_btn = AnimatedButton(QIcon('icons/forward.png'), self)
        forward_btn.clicked.connect(self.forward)
        navbar.addWidget(forward_btn)
        navbar.addWidget(self.create_spacer())

        reload_btn = AnimatedButton(QIcon('icons/reload.png'), self)
        reload_btn.clicked.connect(self.reload)
        navbar.addWidget(reload_btn)
        navbar.addWidget(self.create_spacer())

        home_btn = AnimatedButton(QIcon('icons/home.png'), self)
        home_btn.clicked.connect(self.navigate_home)
        navbar.addWidget(home_btn)
        navbar.addWidget(self.create_spacer())

        new_tab_btn = AnimatedButton(QIcon('icons/new_tab.png'), self)
        new_tab_btn.clicked.connect(self.add_new_tab)
        navbar.addWidget(new_tab_btn)
        navbar.addWidget(self.create_spacer())

        split_view_btn = AnimatedButton(QIcon('icons/split_view.png'), self)
        split_view_btn.clicked.connect(self.split_view)
        navbar.addWidget(split_view_btn)
        navbar.addWidget(self.create_spacer())

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.google_search)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                background-color: #3c3c3c;
                color: white;
                padding: 5px;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #1c7cd5;
            }
        """)
        navbar.addWidget(self.url_bar)

    def create_spacer(self):
        spacer = QWidget()
        spacer.setFixedWidth(10)
        return spacer

    def create_tab(self):
        tab_widget = SplitViewWidget()
        browser = tab_widget.add_webview("https://www.youtube.com")
        i = self.tabs.addTab(tab_widget, "New Tab")
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
        else:
            self.close()

    def add_new_tab(self):
        self.create_tab()

    def navigate_home(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, SplitViewWidget):
            for browser in current_tab.findChildren(QWebEngineView):
                browser.setUrl(QUrl("https://www.google.com"))

    def google_search(self):
        query = self.url_bar.text()
        search_url = f"https://www.google.com/search?q={query}"
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, SplitViewWidget):
            for browser in current_tab.findChildren(QWebEngineView):
                browser.setUrl(QUrl(search_url))

    def update_url(self, q, browser):
        if browser in self.tabs.currentWidget().findChildren(QWebEngineView):
            self.url_bar.setText(q.toString())

    def back(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, SplitViewWidget):
            for browser in current_tab.findChildren(QWebEngineView):
                browser.back()

    def forward(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, SplitViewWidget):
            for browser in current_tab.findChildren(QWebEngineView):
                browser.forward()

    def reload(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, SplitViewWidget):
            for browser in current_tab.findChildren(QWebEngineView):
                browser.reload()

    def split_view(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, SplitViewWidget):
            # Split the current tab into two views
            new_browser = current_tab.add_webview("https://www.google.com")
            self.tabs.currentWidget().update()  # Refresh the layout

app = QApplication(sys.argv)
QApplication.setApplicationName('browssy')
window = MainWindow()
window.setStyleSheet("""
    QMainWindow {
        background-color: black;
    }
    QTabWidget::pane {
        border: none;
    }
    QTabWidget::tab-bar {
        alignment: left;
    }
    QTabBar::tab {
        background-color: #2b2b2b;
        color: white;
        padding: 8px;
        border: none;
    }
    QTabBar::tab:selected {
        background-color: #3c3c3c;
    }
""")
app.exec_()
