import sys, bluetooth
import imaplib
from PyQt4 import QtGui
from PyQt4 import QtCore

def connect():
	# bd_addr = "00:06:66:49:54:31" #BlueSmirf address
	bd_addr = "00:06:66:48:97:57" # RN-42 address
	port = 1
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((bd_addr, port))

def update():
    print "Turn light green"
    sock.send('B') # IF BLUETOOTH ISN'T ON, ERROR MESSAGES WILL SHOW IN CONSOLE


def clear():
    print "Turn off LED"
    sock.send('C') # IF BLUETOOTH ISN'T ON, ERROR MESSAGES WILL SHOW IN CONSOLE

class Login(QtGui.QDialog):

    obj = None

    def __init__(self):
        QtGui.QDialog.__init__(self)

        # set window name and icon
        self.resize(250, 117)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("login.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setWindowTitle('Login')



        # set layout
        grid = QtGui.QGridLayout()
        grid.setSpacing(5)

        userLabel = QtGui.QLabel('Username', self)
        passLabel = QtGui.QLabel('Password', self)
        self.textName = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        grid.addWidget(userLabel, 1, 0)
        grid.addWidget(self.textName, 1, 1)
        grid.addWidget(passLabel, 2, 0)
        grid.addWidget(self.textPass, 2, 1)
        grid.addWidget(self.buttonLogin, 3, 1)

        self.setLayout(grid)

    def handleLogin(self):
        self.accept()
        try:
            #self.obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
            self.obj.login(str(self.textName.text()), str(self.textPass.text()))
        except :
            QtGui.QMessageBox.warning(
                self, 'Error', 'Invalid credentials, please try again.')




class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)
        self.initUI()


    def about(self):
        QtGui.QMessageBox.information(
                self, 'About', '(c) Kevin Shiah for EECE 496, 2013')

    def connectedQuery(self,sock):
        try:
            connect()
            if( sock.send('C') ):
                self.main_widget.btStatus(1)
        except:
           self.statusBar().showMessage('Bluetooth connection failed.')
           self.main_widget.btStatus(0)


    def loginAction(self):
        Login.obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
        print "Logging in"
        self.log = Login()
        Login().exec_()
        loginWindow = Login()
        loginWindow.show()

    def logoutAction(self):
            print "Logging out"
            Login.obj.logout()
            self.statusBar().showMessage('You have logged out.')

    def initUI(self):

        exitAction = QtGui.QAction(QtGui.QIcon('logout.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        aboutAction = QtGui.QAction(QtGui.QIcon('about.png'), 'About', self)
        aboutAction.triggered.connect(self.about)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')
        fileMenu.addAction(exitAction)
        helpMenu.addAction(aboutAction)

		#
		#
		#
		# ...toolbar actions/buttons...
		# Bluetooth connecting
        connectBT = QtGui.QAction(QtGui.QIcon('bluetooth.png'), 'Bluetooth', self)
        connectBT.triggered.connect(self.connectedQuery)
		# Login
        login = QtGui.QAction(QtGui.QIcon('login.png'), 'Login', self)
        login.triggered.connect(self.loginAction)
		# Logout
        logout = QtGui.QAction(QtGui.QIcon('logout.png'), 'Logout', self)
        logout.triggered.connect(self.logoutAction)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(connectBT)
        toolbar.addAction(login)
        toolbar.addAction(logout)

        self.statusBar()
        self.setGeometry(200, 230, 200, 230)
        self.setWindowTitle('NotiMo')
        # set icon of the window
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("mouse.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

class MainWidget(QtGui.QWidget):


    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.initUI()

    def status(self, message):
        self.welcomeText.setText(message)

    def btStatus(self, onOff):
        if( onOff == 1 ):
            self.btText.setText('Bluetooth ON')
        else:
            self.btText.setText('Bluetooth OFF')

    def gmailCheck(self, parent):
        sender = self.sender()
        try:
           Login.obj.select()
           Login.obj.search(None,'UnSeen')
           unread = len(Login.obj.search(None, 'UnSeen')[1][0].split())

           if( unread > 0 ):
               print 'Gmail Unread Count = ', str(unread), ' emails'
               self.window().statusBar().showMessage('You got e-mail!')
               self.status('Gmail Unread Count = ' + str(unread) + ' emails')
               update()
           else:
               self.status('You have no unread e-mails')
               self.window().statusBar().showMessage('')
               clear()
        except AttributeError:
            self.window().statusBar().showMessage('You are not logged into Gmail. Please try again')

    def buttonClicked2(self):
        sender = self.sender()
        clear()

    def initUI(self):

        # setup tab widget
        tab_widget = QtGui.QTabWidget()

        # define tabs
        homeTab = QtGui.QWidget()
        homelayout = QtGui.QHBoxLayout(homeTab)
        homeGridLayout = QtGui.QGridLayout(homeTab)
        # Facebook
        #facebook = QtGui.QPushButton(QtGui.QIcon('facebook.png'), 'Facebook (n/a)', self)
        #facebook.triggered.connect(self.facebookMenu)
		# Twitter
        #twitter = QtGui.QPushButton(QtGui.QIcon('twitter.png'), 'Twitter (n/a)', self)
        #twitter.triggered.connect(self.twitterMenu)

        gmailBtn = QtGui.QPushButton("Check Gmail now", self)
        gmailBtn.setIcon(QtGui.QIcon('gmail.png'))
        gmailBtn.clicked.connect(self.gmailCheck)
        #btn1.move(30, 100)
        clearBtn = QtGui.QPushButton("Clear Notifications", self)
        clearBtn.clicked.connect(self.buttonClicked2)

        #facebook.move(50,130)
        #twitter.move(50,160)

        self.welcomeText = QtGui.QLabel('Welcome to NotiMo! Login to begin checking for notifications.', self)
        self.btText = QtGui.QLabel('Connect to Bluetooth by pressing the icon above', self)

        # stretch(1) centers the widgets
        homeGridLayout.addWidget(self.welcomeText, 1, 0)
        homeGridLayout.addWidget(self.btText, 2, 0)
        homeGridLayout.addWidget(clearBtn, 3, 0)

        homelayout.addStretch(1)
        homelayout.addLayout(homeGridLayout)
        homelayout.addStretch(1)


        gmailTab = QtGui.QWidget()

        fbTab = QtGui.QWidget()

        twTab = QtGui.QWidget()

        # setup automatic updates
        gAutoCheck = QtGui.QCheckBox('Automatic Updates', self)
        gAuto5 = QtGui.QRadioButton('Every 5 minutes')
        gAuto10 = QtGui.QRadioButton('Every 10 minutes')
        gAuto30 = QtGui.QRadioButton('Every 30 minutes')
        # place a grid layout inside a horizontal box layout
        glayout = QtGui.QHBoxLayout(gmailTab)
        gGridlayout = QtGui.QGridLayout(gmailTab)
        gGridlayout.addWidget(gAutoCheck, 1, 0)
        gGridlayout.addWidget(gAuto5, 2, 0)
        gGridlayout.addWidget(gAuto10, 3, 0)
        gGridlayout.addWidget(gAuto30, 4, 0)
        gGridlayout.addWidget(gmailBtn, 5, 0)
        # center the grid layout
        glayout.addStretch(1)
        glayout.addLayout(gGridlayout)
        glayout.addStretch(1)

        # add tabs
        tab_widget.addTab(homeTab, "Home")
        tab_widget.addTab(gmailTab, "Gmail")
        tab_widget.addTab(fbTab, "Facebook")
        tab_widget.addTab(twTab, "Twitter")

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tab_widget)

        self.setLayout(mainLayout)


def main():

    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()



#username = raw_input('Username: ')
#password = raw_input('Password: ')
