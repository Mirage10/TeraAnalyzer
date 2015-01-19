



# PyQt5 examples: http://nullege.com/codes/show/src%40p%40y%40pyqt5-HEAD%40examples%40sql%40cachedtable.py/46/PyQt5.QtWidgets.QTableView/python
import datetime as dt
import itertools as it



SUFFIXES = ['.eps','.tif','.tiff','.jpeg','.jpg',  '.png', '.ppt', '.pptx', '.pdf', '.mts',
            '.doc', '.docx', '.avi', '.ogg','.mov','.wav','.ps','.abw','.txt','.mp3','.mpeg',
            '.webm', '.py']
SUFFIXES = []


DATA_SOURCE_A   = 'sourceA'
DATA_SOURCE_B   = 'sourceB'

# tuple-Komponenten
FILE        = 0
DIRECTORY   = 1
NAME        = 2
SUFFIX      = 3
TIMESTAMP   = 4
YEAR        = 5
MONTH       = 6
YEARMONTH   = 7
SIZE        = 8
HASH        = 9
CNTFILE     = 0
CNTDIR      = 1
CNTSIZE     = 2
ASTERIX     = '*'


BLOCK0 = 0
BLOCK1 = 1
BLOCK2 = 2
BLOCK3 = 3
BLOCK4 = 4
BLOCK5 = 5
BLOCK6 = 6
BLOCK7 = 7



def getkeysuffix(item):
    return item[SUFFIX]
def getkeyyear(item):
    return item[YEAR]
def getkeysuffixyear(item):
    return item[SUFFIX],item[YEAR]
def getkeyyearsuffix(item):
    return item[YEAR],item[SUFFIX]
def getkeyyearmonth(item):
    return item[YEAR],item[MONTH]
def getkeysuffixyearmonth(item):
    return item[SUFFIX],item[YEAR],item[MONTH]
def getkeyyearmonthsuffix(item):
    return item[YEAR],item[MONTH],item[SUFFIX]
def getkeysize(item):
    return int(item[SIZE])




# format with intermediate points for large numbers...
def frmt(numstr):
    ret=''
    n = len(numstr)
    k=0
    while not n == 0:
        k+=1
        ret = numstr[n-1]+ret
        if (k % 3) == 0 and n != 1 :
            ret='.'+ret
        n=n-1
    return ret


class DaoConfig():
    def __init__(self):
       self.__settings = QSettings('TeraAnalyzer', 'TeraAnalyzer')
    def value_get(self,key, defaultvalue):
        # dies ist ein Kommentar
        return self.__settings.value(key, defaultvalue)

    def value_set(self,key, value):
        self.__settings.setValue(key,value)

##

######################################################################
class Dao():

    def __init__(self, datasource):
        self.A=[]
        self.path = ''
        if datasource == DATA_SOURCE_A or datasource == DATA_SOURCE_B:
            conf = DaoConfig()
            self.path = conf.value_get(datasource,'Please enter a Directory')
            print('ein Path: ',self.path)

    def selection(self):
      print('Beginn Selektion')
      self.A=[]
      for root, Dir, File in os.walk(self.path):
        for file in File:
          if file[0] == '.': continue
          a = os.path.join(root, file)
          if '/.' in os.path.join(root, a): continue
          if SUFFIXES and os.path.splitext(a)[1].lower() not in SUFFIXES: continue
          if not os.path.exists(a): continue
          self.A.append( ( str(a),
                           str(os.path.dirname(a)),
                           str(os.path.basename(a)),
                           str(os.path.splitext(a)[1][1:].lower()),
                           str(os.stat(a).st_mtime),
                           str(dt.date.fromtimestamp(os.stat(a).st_mtime).year),
                           str('0'+str(dt.date.fromtimestamp(os.stat(a).st_mtime).month))[-2:],
                           str(dt.date.fromtimestamp(os.stat(a).st_mtime).year)+' '+str(dt.date.fromtimestamp(os.stat(a).st_mtime).month),
                           str(os.stat(a).st_size),
                           str(''))
                           )
      print('Ende Selektion')



    def count_files(self):
      print('Beginn zaehlen')

    # Summe der Dateigroessen ermitteln ...
      size_all=0
      for a in self.A:
        size_all+=int(a[SIZE])

      self.ALL={}
      self.ALL[ASTERIX] = (str(len(self.A)), str(len({a[DIRECTORY]for a in self.A})), str(size_all))


      self.SU = {}
      self.A.sort(key=getkeysuffix)
      for k, F in it.groupby(self.A, getkeysuffix):
         F=list(F)
         self.SU[k] = (len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ]))



      self.YE = {}
      self.A.sort(key=getkeyyear)
      for k, F in it.groupby(self.A, getkeyyear):
         F=list(F)
         self.YE[k] = (len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ]))

      self.SUYE = {}

      self.A.sort(key=getkeysuffixyear)
      for k, F in it.groupby(self.A, getkeysuffixyear):
         F=list(F)
         self.SUYE[k] = (len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ]))

      self.YESU = {}
      self.A.sort(key=getkeyyearsuffix)
      for k, F in it.groupby(self.A, getkeyyearsuffix):
         F=list(F)
         self.YESU[k] = (len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ]))

      self.YEMO = {}
      self.A.sort(key=getkeyyearmonth)
      for k, F in it.groupby(self.A, getkeyyearmonth):
         F=list(F)
         self.YEMO[k] = (len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ]))

      self.SUYEMO = {}
      self.A.sort(key=getkeysuffixyearmonth)
      for k, F in it.groupby(self.A, getkeysuffixyearmonth):
         F=list(F)
         self.SUYEMO[k] = (len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ]))


      self.YEMOSU = {}
      self.A.sort(key=getkeyyearmonthsuffix)
      for k, F in it.groupby(self.A, getkeyyearmonthsuffix):
         F=list(F)
         self.YEMOSU[k] = (len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ]))


      print('Ende Zaehlen')
      print('Das Ergebnis')

    def filter_all(self):
        self.FIL=self.A
        self.FIL.sort(key=getkeysize)
    def filter_suffix(self,suffix):
        self.FIL=[ a for a in self.A if a[SUFFIX] == suffix]
    def filter_year(self,year):
        self.FIL=[ a for a in self.A if a[YEAR] == year]
    def filter_year_month(self,year,month):
        self.FIL=[ a for a in self.A if a[YEAR] == year and a[MONTH] == month  ]
    def filter_suffix_year(self,suffix,year):
        self.FIL=[ a for a in self.A if a[SUFFIX] == suffix and a[YEAR] == year  ]
    def filter_year_suffix(self,year, suffix):
        self.FIL=[ a for a in self.A if a[YEAR] == year and a[SUFFIX] == suffix  ]
    def filter_suffix_year_month(self, suffix, year, month):
        self.FIL=[ a for a in self.A if a[SUFFIX] == suffix and a[YEAR] == year and a[MONTH] == month  ]
    def filter_year_month_suffix(self, year, month, suffix):
        self.FIL=[ a for a in self.A if a[YEAR] == year and a[MONTH] == month and a[SUFFIX] == suffix  ]



##########################################################################
################### UI Entwicklung #######################################
##########################################################################
from PySide.QtGui import *
from PySide.QtCore import *


BRUSH_COMBI      = QBrush(QColor(242, 236, 248))  # hell violett
BRUSH_TARGET     = QBrush(QColor(255, 235, 235))  # pastell rot
BRUSH_SIZE       = QBrush(QColor(229, 249, 255))  # pastell blau
BRUSH_FILE       = QBrush(QColor(255, 242, 229))  # pastell orange
BRUSH_DIRECTORY  = QBrush(QColor(242, 255, 229))  # pastell gruen


# QTItem ueberschreibt den Vergleichsoperator <=, damit die Sortierung der Spalten mit Integer richtig funktioniert;
# ansonsten werden die Integers nach der lexikographischen Reifenfolge sortiert ...
class QTItem(QTableWidgetItem):
    def __init__(self, text, sortKey):
        #call custom constructor with UserType item type
        QTableWidgetItem.__init__(self, text, QTableWidgetItem.UserType)
        self.sortKey = sortKey

    #Qt uses a simple < check for sorting items, override this to use the sortKey
    def __lt__(self, other):
        return self.sortKey < other.sortKey

class Matrix(QTabWidget):

    def __init__(self, dao, files, parent=None):
        super(Matrix, self).__init__(parent)
        self.dao = dao
        self.files = files
        tab1 = self.get_tab_cat_all()
        self.addTab(tab1,'all')
        tab2 = self.get_tab_cat_suffixes()
        self.addTab(tab2,'suffix')
        tab3 = self.get_tab_cat_years()
        self.addTab(tab3,'year')
        tab4 = self.get_tab_cat_year_month()
        self.addTab(tab4,'year month')
        tab5 = self.get_tab_cat_suffix_year()
        self.addTab(tab5,'suffix year')
        tab6 = self.get_tab_cat_year_suffix()
        self.addTab(tab6,'year suffix')
        tab7= self.get_tab_cat_suffix_year_month()
        self.addTab(tab7,'suffix year month')
        tab8= self.get_tab_cat_year_month_suffix()
        self.addTab(tab8,'year month suffix')

        tab1.itemClicked.connect(self.on_matrixfiles_clicked)
        tab2.itemClicked.connect(self.on_matrixfiles_clicked)
        tab3.itemClicked.connect(self.on_matrixfiles_clicked)
        tab4.itemClicked.connect(self.on_matrixfiles_clicked)
        tab5.itemClicked.connect(self.on_matrixfiles_clicked)
        tab6.itemClicked.connect(self.on_matrixfiles_clicked)
        tab7.itemClicked.connect(self.on_matrixfiles_clicked)
        tab8.itemClicked.connect(self.on_matrixfiles_clicked)


        # self.setSortingEnabled(True)
    def get_tab_cat_all(self):
         # all anzeigen

        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(100)
        table.setHorizontalHeaderLabels(['all', '# file', '# directory','# size'])
        value = QTableWidgetItem(ASTERIX)
        # zelle hell violett ...
        value.setBackground(BRUSH_COMBI)

        table.setItem(0, 0, value)
        value = QTItem(self.dao.ALL[ASTERIX][CNTFILE], self.dao.ALL[ASTERIX][CNTFILE] )
        # zelle pastell rot ...
        dat =[ BLOCK0, CNTFILE, ASTERIX ]
        value.setData(5,dat) ##########################
        value.setBackground(BRUSH_TARGET)
        table.setItem(0, 1, value)
        value = QTItem(self.dao.ALL[ASTERIX][CNTDIR],self.dao.ALL[ASTERIX][CNTDIR])
        dat =[ BLOCK0, CNTDIR, ASTERIX ]
        value.setData(5,dat) ##########################
        # zelle pastell rot ...
        value.setBackground(BRUSH_TARGET)
        table.setItem(0, 2, value)
        value = QTItem(frmt(self.dao.ALL[ASTERIX][CNTSIZE]),self.dao.ALL[ASTERIX][CNTSIZE]  )
        dat =[ BLOCK0, CNTSIZE, ASTERIX ]
        value.setData(5,dat) ##########################
        # zelle pastell rot ...
        value.setBackground(BRUSH_SIZE)
        value.setTextAlignment(Qt.AlignRight)
        table.setItem(0, 3, value)
        #table.setSortingEnabled(True)
        return table


    def get_tab_cat_suffixes(self):
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(len(self.dao.SU))
        table.setHorizontalHeaderLabels([ 'suffix','# file', '# directory', '# size'])
        # suffixe anzeigen ...
        K = list(self.dao.SU.keys())
        K.sort()

        for i,s in enumerate(K):
          value = QTableWidgetItem(s)
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTItem(str(self.dao.SU[s][CNTFILE]),self.dao.SU[s][CNTFILE]    )
          dat =[ BLOCK1, CNTFILE, s ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 1, value)
          value = QTItem(str(self.dao.SU[s][CNTDIR]), self.dao.SU[s][CNTDIR]    )
          dat =[ BLOCK1, CNTDIR, s ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...

          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(frmt(str(self.dao.SU[s][CNTSIZE])),self.dao.SU[s][CNTSIZE])
          dat =[ BLOCK1, CNTSIZE, s ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          table.setItem(i, 3, value)
        #table.setSortingEnabled(True)
        return table

    def get_tab_cat_years(self):
        # years anzeigen
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(len(self.dao.YE))
        table.setHorizontalHeaderLabels([ 'year','# file', '# directory', '# size'])
        K = list(self.dao.YE.keys())
        K.sort()
        for i,k in enumerate(K):
          value = QTableWidgetItem(k)
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTItem(str(self.dao.YE[k][CNTFILE]),int(self.dao.YE[k][CNTFILE])          )
          dat =[ BLOCK2, CNTFILE, k ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 1, value)
          value = QTItem(str(self.dao.YE[k][CNTDIR]),self.dao.YE[k][CNTDIR]   )
          dat =[ BLOCK2, CNTDIR, k ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(frmt(str(self.dao.YE[k][CNTSIZE])),self.dao.YE[k][CNTSIZE])
          dat =[ BLOCK2, CNTSIZE, k ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          table.setItem(i, 3, value)
        return table

    def get_tab_cat_year_month(self):
        # year month anzeigen ...
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(len(self.dao.YEMO))
        table.setHorizontalHeaderLabels([ 'year', 'month','# file', '# directory', '# size'])


        K = list(self.dao.YEMO.keys())
        K.sort()
        for i,k in enumerate(K):
          value = QTableWidgetItem(k[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(k[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTItem(str(self.dao.YEMO[k][CNTFILE]),self.dao.YEMO[k][CNTFILE])
          dat =[ BLOCK3, CNTFILE, k[0], k[1] ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(str(self.dao.YEMO[k][CNTDIR]), self.dao.YEMO[k][CNTDIR])
          dat =[ BLOCK3, CNTDIR, k[0],k[1] ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...dao.YEMO[k][CNTDIR]
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(frmt(str(self.dao.YEMO[k][CNTSIZE])),self.dao.YEMO[k][CNTSIZE])
          dat =[ BLOCK3, CNTSIZE, k[0], k[1] ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          table.setItem(i, 4, value)
        return table

    def get_tab_cat_suffix_year(self):
        # suffix years anzeigen
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(len(self.dao.SUYE))
        table.setHorizontalHeaderLabels([ 'suffix', 'year','# file', '# directory', '# size'])


        K = list(self.dao.SUYE.keys())
        K.sort()
        for i,k in enumerate(K):
          value = QTableWidgetItem(k[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(k[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTItem(str(self.dao.SUYE[k][CNTFILE]),self.dao.SUYE[k][CNTFILE])
          dat =[ BLOCK4, CNTFILE, k[0], k[1] ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(str(self.dao.SUYE[k][CNTDIR]),self.dao.SUYE[k][CNTDIR])
          dat =[ BLOCK4, CNTDIR, k[0], k[1] ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(frmt(str(self.dao.SUYE[k][CNTSIZE])),self.dao.SUYE[k][CNTSIZE])
          dat =[ BLOCK4, CNTSIZE, k[0], k[1] ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          table.setItem(i, 4, value)
        return table


    def get_tab_cat_year_suffix(self):
        # years suffix anzeigen

        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(len(self.dao.YESU))
        table.setHorizontalHeaderLabels([ 'year', 'suffix','# file', '# directory', '# size'])

        K = list(self.dao.YESU.keys())
        K.sort()
        for i,k in enumerate(K):
          value = QTableWidgetItem(k[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(k[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTItem(str(self.dao.YESU[k][CNTFILE]),self.dao.YESU[k][CNTFILE])
          dat =[ BLOCK5, CNTFILE, k[0], k[1] ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(str(self.dao.YESU[k][CNTDIR]),self.dao.YESU[k][CNTDIR])
          dat =[ BLOCK5, CNTDIR, k[0], k[1] ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(frmt(str(self.dao.YESU[k][CNTSIZE])),self.dao.YESU[k][CNTSIZE])
          dat =[ BLOCK5, CNTSIZE, k[0], k[1] ]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          table.setItem(i, 4, value)
        return table


    def get_tab_cat_suffix_year_month(self):
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(len(self.dao.SUYEMO))
        table.setHorizontalHeaderLabels([ 'suffix', 'year', 'month','# file', '# directory', '# size'])

        # suffix years month anzeigen
        K = list(self.dao.SUYEMO.keys())
        K.sort()
        for i,k in enumerate(K):
          value = QTableWidgetItem(k[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(k[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTableWidgetItem(k[2])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 2, value)
          value = QTItem(str(self.dao.SUYEMO[k][CNTFILE]),self.dao.SUYEMO[k][CNTFILE])
          dat =[ BLOCK6, CNTFILE, k[0], k[1], k[2]]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(str(self.dao.SUYEMO[k][CNTDIR]),self.dao.SUYEMO[k][CNTDIR])
          dat =[ BLOCK6, CNTDIR, k[0], k[1], k[2]]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 4, value)
          value = QTItem(frmt(str(self.dao.SUYEMO[k][CNTSIZE])),self.dao.SUYEMO[k][CNTSIZE])
          dat =[ BLOCK6, CNTSIZE, k[0], k[1], k[2]]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          table.setItem(i, 5, value)
        return table

    def get_tab_cat_year_month_suffix(self):
        # years month suffix anzeigen
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(len(self.dao.YEMOSU))
        table.setHorizontalHeaderLabels([ 'year', 'month','suffix','# file', '# directory', '# size'])
        K = list(self.dao.YEMOSU.keys())
        K.sort()
        for i,k in enumerate(K):
          value = QTableWidgetItem(k[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(k[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTableWidgetItem(k[2])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 2, value)
          value = QTItem(str(self.dao.YEMOSU[k][CNTFILE]),self.dao.YEMOSU[k][CNTFILE])
          dat =[ BLOCK7, CNTFILE, k[0], k[1], k[2]]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(str(self.dao.YEMOSU[k][CNTDIR]),self.dao.YEMOSU[k][CNTDIR])
          dat =[ BLOCK7, CNTDIR, k[0], k[1], k[2]]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 4, value)
          value = QTItem(frmt(str(self.dao.YEMOSU[k][CNTSIZE])),self.dao.YEMOSU[k][CNTSIZE])
          dat =[ BLOCK7, CNTSIZE, k[0], k[1], k[2]]
          value.setData(5,dat) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          table.setItem(i, 5, value)
        return table




    def on_matrixfiles_clicked(self,item):


        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)

        dat = item.data(5)
        if not dat:
          self.dao.FIL=[]
          self.files.display()
          return
        # es werden nur die Spalten mit # Files beruecksichtigt ...
        if dat[0] == BLOCK0:
          if dat[1] == CNTFILE or dat[1] == CNTDIR or dat[1] == CNTSIZE :
            self.dao.filter_all()
        if dat[0] == BLOCK1:
           if dat[1] == CNTFILE or dat[1] == CNTDIR or dat[1] == CNTSIZE :
             self.dao.filter_suffix(dat[2])
        if dat[0] == BLOCK2:
          if dat[1] == CNTFILE or dat[1] == CNTDIR or dat[1] == CNTSIZE :
             self.dao.filter_year(dat[2])
        if dat[0] == BLOCK3:
          if dat[1] == CNTFILE or dat[1] == CNTDIR or dat[1] == CNTSIZE :
             self.dao.filter_year_month(dat[2],dat[3])
        if dat[0] == BLOCK4:
          if dat[1] == CNTFILE or dat[1] == CNTDIR or dat[1] == CNTSIZE :
             self.dao.filter_suffix_year(dat[2],dat[3])
        if dat[0] == BLOCK5:
          if dat[1] == CNTFILE or dat[1] == CNTDIR or dat[1] == CNTSIZE :
             self.dao.filter_year_suffix(dat[2],dat[3])
        if dat[0] == BLOCK6:
           if dat[1] == CNTFILE or dat[1] == CNTDIR or dat[1] == CNTSIZE :
             self.dao.filter_suffix_year_month(dat[2],dat[3], dat[4])
        if dat[0] == BLOCK7:
           if dat[1] == CNTFILE or dat[1] == CNTDIR or dat[1] == CNTSIZE :
             self.dao.filter_year_month_suffix(dat[2],dat[3], dat[4])


        self.files.display()
        #self.files.setSortingEnabled(True)






import os

class Files(QTableWidget):
    def __init__(self, dao, parent=None):
          super(Files, self).__init__(parent)
          self.dao = dao
          self.itemClicked.connect(self.on_file_clicked)

#
    def display(self):

        self.setColumnCount(8)
        self.setRowCount(len(self.dao.FIL))

        print('clickBegin', len(self.dao.FIL))
        for i, row in enumerate(self.dao.FIL):
          value = QTableWidgetItem(row[SUFFIX])
          value.setText(row[SUFFIX])
          self.setItem(i, 0, value) # spalte suffix
          value = QTableWidgetItem(row[FILE])
          value.setBackground(BRUSH_FILE)
          self.setItem(i, 1, value) # spalte file
          value = QTableWidgetItem(row[NAME])
          value.setData(1,row[FILE])   # bei filename wird intern auch file gespeichert zwecks Positionierung in nemo
          value.setBackground(BRUSH_FILE)
          self.setItem(i, 2, value) # spalte filename
          value = QTableWidgetItem(str(row[DIRECTORY]))
          value.setData(1,str(row[FILE]))   # beim Directory wird intern auch file gespeichert zwecks Positionierung in nemo
          value.setBackground(BRUSH_DIRECTORY)
          self.setItem(i, 3, value) # spalte directory


          value = QTableWidgetItem(row[YEAR])
          self.setItem(i, 4, value)
          value = QTableWidgetItem(row[MONTH])
          self.setItem(i, 5, value)

          value = QTableWidgetItem(row[TIMESTAMP])
          self.setItem(i, 6, value)

          value = QTItem(frmt(row[SIZE]), int(row[SIZE]))
          value.setTextAlignment(Qt.AlignRight)
          self.setItem(i, 7, value)


          # Spaltennamen der Filetabelle setzen
        self.setHorizontalHeaderLabels( ['suffix','file', 'name', 'directory', 'year','month','timestamp' ,'size'])
        print('clickEND')
        self.setSortingEnabled(True)
        #self.show()


    def on_file_clicked(self, item):
        command=''
        if item.column() == 1: # click auf file
          command = 'xdg-open '+'\''+item.text()+'\''
          # das File muss in Hochkommata stehen, da der finename ein blank enthalten kann
        if item.column() == 2: # click auf filename
          # Achtung: data enthaelt  filename incl path, damit nemo in dem Directory auf das File positioniert ...
          command = 'xdg-open '+'\''+item.data(1)+'\''
          # das Directory muss in Hochkommata stehen, da der finename ein blank enthalten kann
        if item.column() == 3: # click auf directory
          # Achtung: data enthaelt  filename incl path, damit nemo in dem Directory auf das File positioniert ...
          command = 'nemo '+'\''+item.data(1)+'\''

        # File oder Ordner anzeigen mit dem richtigen Tool ...
        if command: os.system(command)






class Form(QWidget):


    def __init__(self, daoA, daoB, daoConfig, parent=None):
        super(Form, self).__init__(parent)

        self.daoA = daoA
        self.daoB = daoB
        self.daoConfig = daoConfig




# assemble tab 1 ...
        tab1 = QWidget()
        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        tab1.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente

        files = Files(daoA)
        matrix = Matrix(daoA,files)

        split.addWidget(matrix)
        split.addWidget(files)




 # assemble tab 2 ...
        tab2 = QWidget()
        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        tab2.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente

        files = Files(daoB)
        matrix = Matrix(daoB,files)

        split.addWidget(matrix)
        split.addWidget(files)







# assemble tab 3 ...
        tab3 = QWidget()
        layouttab3 = QFormLayout()
        tab3.setLayout(layouttab3)


        self.editA = QLineEdit()
        ss = self.daoConfig.value_get( 'sourceA' , 'Please select a Directory' )
        self.editA.setText(ss)

        butA = QPushButton('Source A')
        butA.clicked.connect(self.on_button_clickedA)
        layouttab3.addRow(butA, self.editA)

        self.editB = QLineEdit()
        ss = self.daoConfig.value_get('sourceB', 'Please select a Directory')
        self.editB.setText(ss)

        butB = QPushButton('Source B')
        butB.clicked.connect(self.on_button_clickedB)
        layouttab3.addRow(butB, self.editB)











# assemble topwidget ...

#        Menue
#        menu_bar = QMenuBar()
#        operations = menu_bar.addMenu("&Operations")
#        help       = menu_bar.addMenu("&Help")
#
#

        action_scope       = QAction('Scope', self)
        action_retrieve    = QAction('Retrieve', self)
        action_indexing    = QAction('Indexing', self)
        action_duplicates  = QAction('Duplicates', self)
        action_trash       = QAction('Trash', self)
        action_advanced    = QAction('Advanced', self)
        action_scope.triggered.connect(self.submitContact)
#       operations.addAction(action_scope)
#       operations.addAction(action_indexing)
#       operations.addAction(action_duplicates)
#       operations.addAction(action_trash)



        toolbar = QToolBar()
        toolbar.addAction(action_scope)
        toolbar.addAction(action_retrieve)
        toolbar.addAction(action_indexing)
        toolbar.addAction(action_duplicates)
        toolbar.addAction(action_trash)
        toolbar.addAction(action_advanced)


        tabwid = QTabWidget()




        tabwid.addTab(tab1,'Space A')
        tabwid.addTab(tab2,'Space B')
        tabwid.addTab(tab3,'Config')


        toplayout = QVBoxLayout(self)
        toplayout.addWidget(toolbar)
        toplayout.addWidget(tabwid)


#       self.matrix.itemClicked.connect(self.on_matrixfiles_clicked)
#        self.files.itemClicked.connect(self.on_file_clicked)
        self.setWindowTitle("Tera-Analyzer")




    def on_button_clickedA(self):
        ss = QFileDialog(self,"Bitte Directory auswaehlen","/home/user").getExistingDirectory(self)
        if ss:
          self.editA.setText(ss)
          self.daoConfig.value_set('sourceA',ss)

    def on_button_clickedB(self):
        ss = QFileDialog(self,'Bitte Directory auswaehlen','/home/user').getExistingDirectory(self)
        if ss:
          self.editB.setText(ss)
          self.daoConfig.value_set('sourceB',ss)



    ################################################################


    ################################################################
    def submitContact(self):
        #name = self.nameLine.text()

        #if name == "":
            QMessageBox.information( self, "Empty Field",
                                    "Please enter a name and address.")
            return
        #else:
         #   QMessageBox.information(self, "Success!",
          #                          "Hello %s !" % name)



import sys
import hashlib






daoA = Dao(DATA_SOURCE_A)
daoA.selection()
daoA.count_files()

daoB = Dao(DATA_SOURCE_B)
daoB.selection()
daoB.count_files()
daoConfig = DaoConfig()


#for a in daoo.A:B
#  f = open(a[FILE],'rb')

  #h = hashlib.md5()
  #h.update(f.read())
  #hash = h.hexdigest()
  #print(hash)
  #f.close()





app = QApplication(sys.argv)
screen = Form( daoA, daoB, daoConfig )
screen.show()
sys.exit(app.exec_())















