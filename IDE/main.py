#                ______________________________ 
#_______________/ LIBRARIES 
 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5 import *
from os.path import splitext
import basic
 
#                ______________________________ 
#_______________/ CLASS LINENUMBER
class LineNumberArea(QWidget): 
    def __init__(self, editor): 
        QWidget.__init__(self, parent=editor) 
        self.codeEditor = editor 
 
    def sizeHint(self): 
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0) 
 
    def paintEvent(self, event): 
        self.codeEditor.lineNumberAreaPaintEvent(event) 
#                ______________________________ 
#_______________/ CLASS MAIN WINDOW    
class Ui_MainWindow(QMainWindow):
    #           _____________________________ 
    #__________/ WINDOW CONSTRUCTOR
    def setupUi(self, mainWindow):  
        windowX = 1366 
        windowY = 768 
        mainWindow.setGeometry(0, 0, windowX, windowY) 
        mainWindow.setWindowTitle("Wrinting Machine") 
        #mainWindow.setStyleSheet("background-color : white") 
        self.dir_path = r'C:\GitHub'
        self.cur_path = None
         
        #           _____________________________ 
        #__________/ WINDOW OBJECTS 
         
        self.menuBar = QMenuBar(mainWindow)   #Menu Bar 
        self.menuBar.setGeometry(QRect(0, 0, windowX, 21)) 
        mainWindow.setMenuBar(self.menuBar) 
 
        self.menuFile = QMenu(self.menuBar)   #Menu File 
        self.menuFile.setTitle("File") 
        self.menuBar.addAction(self.menuFile.menuAction()) 
         
        self.menuRun = QMenu(self.menuBar)    #Menu Run 
        self.menuRun.setTitle("Run") 
        self.menuBar.addAction(self.menuRun.menuAction()) 
 
        self.actionNew_File = QAction(mainWindow, triggered = self.new_file) #Action New File 
        self.actionNew_File.setText("New File") 
        self.menuFile.addAction(self.actionNew_File) 
         
        self.actionOpen = QAction(mainWindow, triggered = self.open_new_file) #Action Open  
        self.actionOpen.setText("Open") 
        self.menuFile.addAction(self.actionOpen) 
         
        self.actionSave = QAction(mainWindow, triggered = self.save_current_file) #Action Save 
        self.actionSave.setText("Save") 
        self.menuFile.addAction(self.actionSave) 
 
        self.actionSave_as = QAction(mainWindow, triggered = self.save_current_file_as)  #Action Save as 
        self.actionSave_as.setText("Save As...") 
        self.menuFile.addAction(self.actionSave_as) 
 
        self.actionCompile = QAction(mainWindow, triggered = self.Compile)  #Action Compile 
        self.actionCompile.setText("Compile") 
        self.menuRun.addAction(self.actionCompile)
 
        self.actionBuild = QAction(mainWindow, triggered = self.Compile_Run)    #Action Compile and Run 
        self.actionBuild.setText("Compile and Run") 
        self.menuRun.addAction(self.actionBuild) 

 
        self.actionExit = QAction(mainWindow, triggered = self.closeEvent) #Action Exit 
        self.actionExit.setText("Exit") 
        self.menuFile.addAction(self.actionExit) 
 
        self.actionSave_and_Exit = QAction(mainWindow)    #Action Save and Exit 
        self.actionSave_and_Exit.setText("Save and Exit") 
         
         
        self.statusBar = QStatusBar(mainWindow)   #Status Bar 
        mainWindow.setStatusBar(self.statusBar) 
        self.statusBar.showMessage("This is status bar") 
        #self.statusBar.setStyleSheet("background-color : gray") 
         
        self.centralWidget = QWidget(mainWindow)  #Central Widget 
        mainWindow.setCentralWidget(self.centralWidget) 
         
        self.groupBox = QGroupBox(self.centralWidget) #Code Group Box 
        self.groupBox.setGeometry(QRect(5, 5, round((windowX/100)*70.84) , round((windowY/100)*74.45))) 
        self.groupBox.setTitle("Untitled File") 
        #self.groupBox.setStyleSheet("background-color : white") 
 
        self.codeText = QPlainTextEdit(self.groupBox) #Code Text 
        self.codeEditor = CodeEditor(self.codeText) 
        self.codeText.setGeometry(QRect(5, 20, round((windowX/100)*70), round((windowY/100)*71.13))) 
        self.codeEditor.setGeometry(QRect(0, 0, round((windowX/100)*70) , round((windowY/100)*71.13))) 
         
         
        self.explorerBox = QGroupBox(self.centralWidget)  #Explorer Group Box 
        self.explorerBox.setGeometry(QRect(round((windowX/100)*71.67), 5 , round((windowX/100)*27.91), round((windowY/100)*74.45))) 
        self.explorerBox.setTitle("File Explorer") 
        #self.explorerBox.setStyleSheet("background-color : white") 
 
        self.model = QFileSystemModel(mainWindow) 
        self.model.setRootPath(self.dir_path)
 
        self.treeView = QTreeView(self.explorerBox)   #File Tree View 
        self.treeView.setGeometry(QRect(5, 20, round((windowX/100)*27.08), round((windowY/100)*71.23))) 
        self.treeView.setModel(self.model) 
        self.treeView.setRootIndex(self.model.index(self.dir_path)) 
        self.treeView.setColumnWidth(0, round((windowX/100)*27.08)) 
        self.treeView.clicked.connect(self.on_treeView_clicked)
 
        self.tabWidget = QTabWidget(self.centralWidget)   #Tab Widget 
        self.tabWidget.setGeometry(QRect(1, round((windowY/100)*74.45), windowX, round((windowY/100)*21))) 
        self.tabWidget.setCurrentIndex(0) 
 
        self.Errors_TAB = QWidget()   #Errors Tab 
        self.tabWidget.addTab(self.Errors_TAB, "Errors")
        self.error_Text = QPlainTextEdit(self.Errors_TAB) 
        self.error_Text.setReadOnly(True)
        self.error_Text.setStyleSheet("font-family: Courier")
        self.error_Text.setGeometry(QRect(0, 0, windowX - 6 , round((windowY/100)*18.11)))

        self.Output_TAB = QWidget()   #Output Tab 
        self.tabWidget.addTab(self.Output_TAB, "Output") 
        self.output_Text = QPlainTextEdit(self.Output_TAB)
        self.output_Text.setReadOnly(True)
        self.output_Text.setStyleSheet("font-family: Courier")
        self.output_Text.setGeometry(QRect(0, 0, windowX - 6 , round((windowY/100)*18.11)))

        self.Terminal_TAB = QWidget()
        self.tabWidget.addTab(self.Terminal_TAB, "Terminal")
        self.terminal_Console = QPlainTextEdit(self.Terminal_TAB)
        self.terminal_Console.setStyleSheet("font-family: Courier")
        self.terminal_Console.setGeometry(QRect(0, 0, windowX - 6 , round((windowY/100)*18.11)))
    
        QMetaObject.connectSlotsByName(mainWindow)
        #           _____________________________ 
        #__________/ SHORTCUTS
        
        self.open_new_file_shortcut = QShortcut(QKeySequence('Ctrl+O'), self.centralWidget) #Open New File
        self.open_new_file_shortcut.activated.connect(self.open_new_file)
        
        self.save_current_file_shortcut = QShortcut(QKeySequence('Ctrl+S'), self.centralWidget)   #Save File
        self.save_current_file_shortcut.activated.connect(self.save_current_file)

        self.compile_and_run_shortcut = QShortcut(QKeySequence('F5'), self.centralWidget) #Compile and Run
        self.compile_and_run_shortcut.activated.connect(self.Compile_Run)

        self.compile_shortcut = QShortcut(QKeySequence('Ctrl+F5'), self.centralWidget) #Compile
        self.compile_shortcut.activated.connect(self.Compile)
    #           _____________________________ 
    #__________/ NEW FILE SHORTCUT FUNCTION
    def new_file(self):
        if self.cur_path or (self.codeEditor.blockCount != 1):
            messageBox = QMessageBox()
            title = "Writing Machine IDE"
            message = "Do you want to save changes to " + self.groupBox.title() + "?"
            reply = messageBox.question(self, title, message, messageBox.Yes | messageBox.No | messageBox.Cancel, messageBox.Cancel)
            if reply == messageBox.Yes:
                self.save_current_file()
                self.cur_path = None
                self.codeEditor.clear()
                self.groupBox.setTitle("Untitled File")
            elif reply == messageBox.No:
                self.cur_path = None
                self.codeEditor.clear()
                self.groupBox.setTitle("Untitled File")  
    #           _____________________________ 
    #__________/ OPEN NEW FILE SHORTCUT FUNCTION
    def open_new_file(self):
        self.dir_path, filter_type = QFileDialog.getOpenFileName(self.centralWidget, "Open new file", "", "Writing Machine Code (*.wrma)")
        if self.dir_path:
            with open(self.dir_path, "r") as f:
                file_contents = f.read()
                self.groupBox.setTitle(self.dir_path)
                self.codeEditor.clear()
                self.codeEditor.insertPlainText(file_contents)
                self.cur_path = self.dir_path
        else:
            self.invalid_path_alert_message()
    #           _____________________________ 
    #__________/ SAVE FILE SHORTCUT FUNCTION 
    def save_current_file(self):
        if not self.cur_path:
            new_file_path, filter_type = QFileDialog.getSaveFileName(self.centralWidget, "Save this file as...", "", "Writing Machine Code (*.wrma)")
            if new_file_path:
                self.cur_path = new_file_path
            else:
                self.invalid_path_alert_message()
                return False
        file_contents = self.codeEditor.toPlainText()
        with open(self.cur_path, "w") as f:
            f.write(file_contents)
        self.groupBox.setTitle(self.cur_path)
    #           _____________________________ 
    #__________/ SAVE AS FILE SHORTCUT FUNCTION
    def save_current_file_as(self):
        new_file_path, filter_type = QFileDialog.getSaveFileName(self.centralWidget, "Save this file as...", "", "Writing Machine Code (*.wrma)")
        if new_file_path:
            self.cur_path = new_file_path
        else:
            self.invalid_path_alert_message()
            return False
        file_contents = self.codeEditor.toPlainText()
        with open(self.cur_path, "w") as f:
            f.write(file_contents)
        self.groupBox.setTitle(self.cur_path)
    #           _____________________________ 
    #__________/ CLOSE EVENT FUNCTION
    def closeEvent(self, event):
        messageBox = QMessageBox()
        title = "Quit Application?"
        message = "WARNING !!\n\n If you quit without saving, any changes made to the file will be lost.\n\n Save file before quitting?"
        reply = messageBox.question(self, title, message, messageBox.Yes | messageBox.No | messageBox.Cancel, messageBox.Cancel)
        if reply == messageBox.Yes:
            return_value = self.save_current_file()
            if return_value == False:
                event.ignore()
        elif reply == messageBox.No:
            event.accept()
        else:
            event.ignore()
    #           _____________________________ 
    #__________/ INVALID PATH FUNCTION
    def invalid_path_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Invalid file")
        messageBox.setText("Selected filename or path is not valid. Please select a valid file.")
        messageBox.exec()
    #           _____________________________ 
    #__________/ COMPILE FUNCTION
    def Compile(self):
        self.compile_Text = self.codeEditor.toPlainText()
        result, error = basic.run('<stdin>', self.compile_Text)
        self.error_Text.clear()
        self.output_Text.clear()
        if(error):
            self.error_Text.insertPlainText(error.as_string())
        else:
            self.error_Text.insertPlainText("No errors found")
        self.tabWidget.setCurrentIndex(0)
    #           _____________________________ 
    #__________/ COMPILE AND RUN FUNCTION 
    def Compile_Run(self):
        sys.stdout = open("log.txt", "w") 
        self.compile_Text = self.codeEditor.toPlainText()
        result, error = basic.run('<stdin>', self.compile_Text)
        self.error_Text.clear()
        self.output_Text.clear()
        if(error):   
            self.error_Text.insertPlainText(error.as_string())
            self.tabWidget.setCurrentIndex(0)
        else:
            self.error_Text.insertPlainText("No errors found")
            if(len(result.elements) == 1):
                self.output_Text.insertPlainText(repr(result.elements[0]))
            else:
                self.output_Text.insertPlainText(repr(result))
            sys.stdout.close()
            with open("log.txt", "r") as f:
                file_contents = f.read()
                self.terminal_Console.clear()
                self.terminal_Console.insertPlainText(file_contents)
                self.tabWidget.setCurrentIndex(2)
    #           _____________________________ 
    #__________/ TREEVIEW CLICKED FUNCTION
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)
        fileName, extension = splitext(fileName)
        if extension == ".wrma":
            with open(filePath, "r") as f:
                file_contents = f.read()
                self.groupBox.setTitle(filePath)
                self.codeEditor.clear()
                self.codeEditor.insertPlainText(file_contents)
                self.cur_path = filePath
#           _____________________________ 
#__________/ CODE EDITOR
class CodeEditor(QPlainTextEdit): 
    def __init__(self, parent=None): 
        QPlainTextEdit.__init__(self, parent) 
        self.lineNumberArea = LineNumberArea(self) 
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth) 
        self.updateRequest.connect(self.updateLineNumberArea) 
        self.cursorPositionChanged.connect(self.highlightCurrentLine) 
        self.updateLineNumberAreaWidth(0) 
        self.highlightCurrentLine() 
 
    def lineNumberAreaPaintEvent(self, event): 
        painter = QPainter(self.lineNumberArea) 
        painter.fillRect(event.rect(), Qt.lightGray) 
 
        block = self.firstVisibleBlock() 
        blockNumber = block.blockNumber(); 
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top() 
        bottom = top + self.blockBoundingRect(block).height() 
 
        while block.isValid() and top <= event.rect().bottom(): 
            if block.isVisible() and bottom >= event.rect().top(): 
                number = str(blockNumber + 1) 
                painter.setPen(Qt.black) 
                painter.drawText(0, round(top), round(self.lineNumberArea.width()),  
                    self.fontMetrics().height(), 
                    Qt.AlignRight, number) 
            block = block.next() 
            top = bottom 
            bottom = top + self.blockBoundingRect(block).height() 
            blockNumber += 1 
 
    def lineNumberAreaWidth(self): 
        digits = len(str(self.blockCount())) 
        space = 3 + self.fontMetrics().width('9')*digits 
        return space 
 
    def resizeEvent(self, event): 
        QPlainTextEdit.resizeEvent(self, event) 
        cr = self.contentsRect() 
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())) 
 
    @pyqtSlot(int) 
    def updateLineNumberAreaWidth(self, newBlockCount): 
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0); 
 
    @pyqtSlot() 
    def highlightCurrentLine(self): 
        extraSelections = [] 
        if not self.isReadOnly(): 
            selection = QTextEdit.ExtraSelection() 
            lineColor = QColor(Qt.blue).lighter(160) 
            selection.format.setBackground(lineColor) 
            selection.format.setProperty(QTextFormat.FullWidthSelection, True) 
            selection.cursor = self.textCursor() 
            selection.cursor.clearSelection() 
            extraSelections.append(selection) 
        self.setExtraSelections(extraSelections) 
 
    @pyqtSlot(QRect, int) 
    def updateLineNumberArea(self, rect, dy): 
        if dy: 
            self.lineNumberArea.scroll(0, dy) 
        else: 
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height()) 
        if rect.contains(self.viewport().rect()): 
            self.updateLineNumberAreaWidth(0) 
#                ______________________________ 
#_______________/ START  
if __name__ == "__main__": 
    import sys 
    app = QApplication(sys.argv) 
    mainWindow = QMainWindow() 
    ui = Ui_MainWindow() 
    ui.setupUi(mainWindow) 
    mainWindow.show() 
    sys.exit(app.exec_()) 
