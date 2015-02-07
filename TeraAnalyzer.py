



# PyQt5 examples: http://nullege.com/codes/show/src%40p%40y%40pyqt5-HEAD%40examples%40sql%40cachedtable.py/46/PyQt5.QtWidgets.QTableView/python
from datetime import date
import itertools as it
import collections as co
import os
import sys



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
LEVEL       = 9
HASH        = 10


ASTERIX     = '*'





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
def getkeylevel(item):
    return int(item[LEVEL])
def getkeysize(item):
    return int(item[SIZE])
def getkeyhash(item):
    return item[HASH]
def getkey2(item):
    return item[2]


# format with intermediate points for large numbers...
def frmt(numstr):
    numstr=str(numstr)
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


import itertools

## little change
######################################################################
class Dao():


    def diff(A,B):
    # dient nur als Prototyp ...
        L =[]
        M =[]
        R =[]
        A.sort()
        B.sort()
        i = 0
        j = 0

        while True:
            try: a=A[i]
            except:
              R.extend(B[j:])
              break
            try: b=B[j]
            except:
              L.extend(A[i:])
              break

            if a > b:
                R.append(b)
                j+=1
                continue
            if a == b:
                M.append(a)
                i+=1
                j+=1
                continue
            if a < b:
                L.append(a)
                i+=1
                continue
        return L, M , R




















    def difference(daoa, daob):
        # dient nur als Prototyp ...
        daol=Dao()
        daom=Dao()
        daor=Dao()
        daoa.A.sort(key=getkeysize)
        daob.A.sort(key=getkeysize)
        lena = len(daoa.A)
        lenb = len(daob.A)
        i = 0
        j = 0

        while True:
            try:
              a=daoa.A[i]
            except:
              daor.A.extend(daob.A[j:])
              break
            try: b=daob.A[j]
            except:
              daol.A.extend(daoa.A[i:])
              break

            if a[SIZE] > b[SIZE]:
                daor.A.append(b)
                j+=1
                continue
            if a[SIZE] == b[SIZE]:
                print('Gleichheit')
                daom.A.append(a)
                i+=1
                j+=1

                continue
            if a[SIZE] < b[SIZE]:
                daol.A.append(a)
                i+=1
                continue
        return daol, daom , daor





    def __init__(self, datasource=None):
        self.A=[]
        self.FIL=[]
        self.path = ''
        if datasource == DATA_SOURCE_A or datasource == DATA_SOURCE_B:
            conf = DaoConfig()
            self.path = conf.value_get(datasource,'Please enter a Directory')
            print('ein Path: ',self.path)

    def getkeylen(self,item):
        s=self.A[item][SIZE]
        return s
    def getkeyhash(self,item):
        s=self.A[item][HASH]
        return s


    def dedub(self):

        # Achtung: Auf A keine Sortierung machen. Alle Pointer erwarten die anfangs gemachte Reihenfolge ...


        self.B=[i for i, a in enumerate(self.A)]
        self.B.sort(key=self.getkeylen)
        # in R sollen die pointer auf A stehen, die die gleichen Längen haben...
        R=[]
        F=[]

        flag=False


        for i, b in enumerate(self.B):
            if i==0: continue
            x=self.A[self.B[i-1]][SIZE]
            y=self.A[b][SIZE]
            if x==y:
              R.append(self.B[i-1])
              flag=True
              continue

            if flag:
               R.append(self.B[i-1])
               flag=False

        if flag:
        # falls Gleichheit bis ans Ende besteht, den letzten Eintrag noch mitnehmen
            R.append(self.B[-1])

        # hash werte fuer genau die Elemente in R berechnen. Hash werte werden auf Ebene von A gespeichert
        for r in R:
            if self.A[r][SIZE]==0:
                self.A[r][HASH] = 0
                continue
            with open(self.A[r][FILE],'rb') as f:

                h = hash(f.read())
                #print(h)
                if h < 0: h=-h
                self.A[r][HASH] = h
                print(self.A[r][HASH])


        # Phase II: weitere Einschränkung von R ...
        # analog wie oben die duplikatermittlung auf hash, statt auf len ...

        R.sort(key=self.getkeyhash)
        # in S sollen die pointer auf A stehen, die die gleichen hashes(laengen) haben...
        S=[]

        flag=False


        for i, r in enumerate(R):
            if i==0: continue
            x=self.A[R[i-1]][HASH]
            y=self.A[r][HASH]
            if x==y:
              S.append(R[i-1])
              flag=True
              continue
            if flag:
               S.append(R[i-1])
               flag=False

        if flag:
        # falls Gleichheit bis ans Ende besteht, den letzten Eintrag noch mitnehmen
            S.append(R[-1])



        # Achtung: hier F aufbauen, die aus Unikaten besteht

        print('ERGE:  ',[self.A[b][SIZE] for b in self.B])

        S.sort(key=self.getkeylen)
        print('RR= ',[self.A[s][SIZE] for s in S])
        print(S)
        R= [self.A[s] for s in S]
        return R




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
          self.A.append( [ str(a),
                           str(os.path.dirname(a)),
                           str(os.path.basename(a)),
                           str(os.path.splitext(a)[1][1:].lower()),
                           str(os.stat(a).st_mtime),
                           str(date.fromtimestamp(os.stat(a).st_mtime).year),
                           str('0'+str(date.fromtimestamp(os.stat(a).st_mtime).month))[-2:],
                           str(date.fromtimestamp(os.stat(a).st_mtime).year)+' '+str(date.fromtimestamp(os.stat(a).st_mtime).month),
                           os.stat(a).st_size,
                           a.count('/')-1,  #level
                           0, ] )                 #hash


      print('Ende Selektion')



    def count_files(self):
      print('Beginn zaehlen')

    # Summe der Dateigroessen ermitteln ...
      size_all=0
      for a in self.A:
        size_all+=int(a[SIZE])

      self.ALL=[]
      self.ALL.append((ASTERIX ,str(len(self.A)), str(len({a[DIRECTORY]for a in self.A})), str(size_all)))


      self.SU = []
      self.A.sort(key=getkeysuffix)
      for k, F in it.groupby(self.A, getkeysuffix):
         F=list(F)
         self.SU.append((k , len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))



      self.YE = []
      self.A.sort(key=getkeyyear)
      for k, F in it.groupby(self.A, getkeyyear):
         F=list(F)
         self.YE.append((k,len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

      self.SUYE = []

      self.A.sort(key=getkeysuffixyear)
      for k, F in it.groupby(self.A, getkeysuffixyear):
         F=list(F)
         self.SUYE.append((k[0],k[1],len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

      self.YESU = []
      self.A.sort(key=getkeyyearsuffix)
      for k, F in it.groupby(self.A, getkeyyearsuffix):
         F=list(F)
         self.YESU.append((k[0],k[1],len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

      self.YEMO = []
      self.A.sort(key=getkeyyearmonth)
      for k, F in it.groupby(self.A, getkeyyearmonth):
         F=list(F)
         self.YEMO.append((k[0],k[1], len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

      self.SUYEMO = []
      self.A.sort(key=getkeysuffixyearmonth)
      for k, F in it.groupby(self.A, getkeysuffixyearmonth):
         F=list(F)
         self.SUYEMO.append((k[0],k[1],k[2],len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))


      self.YEMOSU = []
      self.A.sort(key=getkeyyearmonthsuffix)
      for k, F in it.groupby(self.A, getkeyyearmonthsuffix):
         F=list(F)
         self.YEMOSU.append(( k[0],k[1],k[2], len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))


      self.LE = []
      self.A.sort(key=getkeylevel)
      for k, F in it.groupby(self.A, getkeylevel):
         F=list(F)
         self.LE.append((k , len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))


      print('Ende Zählen')
      print('Das Ergebnis')

    def filter_all(self):
        self.FIL=[ i for i, a in enumerate (self.A)]

    def filter_suffix(self,suffix):
        self.FIL=[ i for i, a in enumerate(self.A) if a[SUFFIX] == suffix]
    def filter_year(self,year):
        self.FIL=[ i for i, a in enumerate(self.A) if a[YEAR] == year]
    def filter_year_month(self,year,month):
        self.FIL=[ i for i, a in enumerate(self.A) if a[YEAR] == year and a[MONTH] == month  ]
    def filter_suffix_year(self,suffix,year):
        self.FIL=[ i for i, a in enumerate(self.A) if a[SUFFIX] == suffix and a[YEAR] == year  ]
    def filter_year_suffix(self,year, suffix):
        self.FIL=[ i for i, a in enumerate(self.A) if a[YEAR] == year and a[SUFFIX] == suffix  ]
    def filter_suffix_year_month(self, suffix, year, month):
        self.FIL=[ i for i, a in enumerate(self.A) if a[SUFFIX] == suffix and a[YEAR] == year and a[MONTH] == month  ]
    def filter_year_month_suffix(self, year, month, suffix):
        self.FIL=[ i for i, a in enumerate(self.A) if a[YEAR] == year and a[MONTH] == month and a[SUFFIX] == suffix  ]
    def filter_level(self,level):
        self.FIL=[ i for i, a in enumerate(self.A) if a[LEVEL] == level]




#

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


class Tab_All(QWidget):
    def __init__(self, dao, parent=None):
        super(Tab_All, self).__init__(parent)
        # all anzeigen
        self.dao = dao
        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        self.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.table = QTableWidget()
        self.table.itemClicked.connect(self.on_kpi_clicked)
        split.addWidget(self.table)

        self.files_all = Files(dao)
        split.addWidget( self.files_all)



        self.table.setSortingEnabled(True)
        self.table.setColumnCount(30)
        self.table.setRowCount(100)
        self.table.setHorizontalHeaderLabels(['all', '# file', '# directory','# size'])
        self.set_content()
        #self.set_tab_content_all(tab)
        #tab.xxx=self.set_tab_content_all



    def set_content(self):
        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3

        for i,s in enumerate(self.dao.ALL):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(0, 0, value)
          value = QTItem(str(s[CNTFILE]), s[CNTFILE] )
          # zelle pastell rot ...
          value.setData(5,i) ##########################
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(0, 1, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(0, 2, value)
          value = QTItem(frmt(s[CNTSIZE]),s[CNTSIZE]  )
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(0, 3, value)
          #table.setSortingEnabled(True)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_all.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.ALL[index]
        self.dao.filter_all()
        self.files_all.display()
        #self.files.setSortingEnabled(True)

class Tab_SU(QWidget):
    def __init__(self, dao, parent=None):
        super(Tab_SU, self).__init__(parent)

#tab_su.itemClicked.connect(self.on_matrixfiles_clicked_su)
        self.dao = dao

        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        self.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.table = QTableWidget()
        self.table.itemClicked.connect(self.on_kpi_clicked)
        split.addWidget(self.table)

        self.files_su = Files(self.dao)
        split.addWidget( self.files_su)

        self.table.setSortingEnabled(True)
        self.table.setColumnCount(30)
        self.table.setRowCount(len(self.dao.SU))
        self.table.setHorizontalHeaderLabels([ 'suffix','# file', '# directory', '# size'])
        self.set_content()

    def set_content(self):
        # suffixe anzeigen ...
        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3

        for i,s in enumerate(self.dao.SU):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE]  )
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 1, value)
          value = QTItem(str(s[CNTDIR]), s[CNTDIR]    )
          value.setData(5,i) ##########################
          # zelle pastell rot ...

          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 3, value)
        #table.setSortingEnabled(True)


    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_su.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.SU[index]
        self.dao.filter_suffix(s[0])
        self.files_su.display()
        #self.files.setSortingEnabled(True)

class Tab_YE(QWidget):
    def __init__(self, dao, parent=None):
        super(Tab_YE, self).__init__(parent)
        self.dao = dao
        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        self.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.table = QTableWidget()
        self.table.itemClicked.connect(self.on_kpi_clicked)
        split.addWidget(self.table)

        self.files_ye = Files(self.dao)
        split.addWidget( self.files_ye)



        self.table.setSortingEnabled(True)
        self.table.setColumnCount(30)
        self.table.setRowCount(len(self.dao.YE))
        self.set_content()

    def set_content(self):
        # years anzeigen
        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3

        self.table.setHorizontalHeaderLabels([ 'year','# file', '# directory', '# size'])
        for i,s in enumerate(self.dao.YE):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE]        )
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 1, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR]   )
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 3, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_ye.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.YE[index]
        self.dao.filter_year(s[0])
        self.files_ye.display()
        #self.files.setSortingEnabled(True)

class Tab_YEMO(QWidget):
    def __init__(self, dao, parent=None):
        super(Tab_YEMO, self).__init__(parent)
         # year month anzeigen ...

        self.dao = dao


        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        self.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.table = QTableWidget()
        self.table.itemClicked.connect(self.on_kpi_clicked)
        split.addWidget(self.table)

        self.files_yemo = Files(self.dao)
        split.addWidget( self.files_yemo)

        self.table.setSortingEnabled(True)
        self.table.setColumnCount(30)
        self.table.setRowCount(len(self.dao.YEMO))
        self.table.setHorizontalHeaderLabels([ 'year', 'month','# file', '# directory', '# size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4


        for i,s in enumerate(self.dao.YEMO):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 1, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(str(s[CNTDIR]), s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...dao.YEMO[k][CNTDIR]
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)

          self.table.setItem(i, 4, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_yemo.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.YEMO[index]
        self.dao.filter_year_month(s[0],s[1])
        self.files_yemo.display()
        #self.files.setSortingEnabled(True)

class Tab_SUYE(QWidget):
    def __init__(self, dao, parent=None):
        super(Tab_SUYE, self).__init__(parent)
         # year month anzeigen ...

        self.dao = dao
          # suffix years anzeigen

        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        self.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.table = QTableWidget()
        self.table.itemClicked.connect(self.on_kpi_clicked)
        split.addWidget(self.table)

        self.files_suye= Files(self.dao)
        split.addWidget( self.files_suye)


        self.table.setSortingEnabled(True)
        self.table.setColumnCount(30)
        self.table.setRowCount(len(self.dao.SUYE))
        self.table.setHorizontalHeaderLabels([ 'suffix', 'year','# file', '# directory', '# size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4


        for i,s in enumerate(self.dao.SUYE):
          value = QTableWidgetItem(s[0])
          # self.files.setSortingEnabled(False)
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 1, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 4, value)


    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_suye.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.SUYE[index]
        self.dao.filter_suffix_year(s[0],s[1])
        self.files_suye.display()
        #self.files.setSortingEnabled(True)



class Tab_YESU(QWidget):
    def __init__(self, dao, parent=None):
        super(Tab_YESU, self).__init__(parent)
         # year month anzeigen ...
        self.dao = dao
         # years suffix anzeigen


        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        self.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.table = QTableWidget()
        self.table.itemClicked.connect(self.on_kpi_clicked)
        split.addWidget(self.table)

        self.files_yesu = Files(self.dao)
        split.addWidget( self.files_yesu)

        self.table.setSortingEnabled(True)
        self.table.setColumnCount(30)
        self.table.setRowCount(len(self.dao.YESU))
        self.table.setHorizontalHeaderLabels([ 'year', 'suffix','# file', '# directory', '# size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4

        for i,s in enumerate(self.dao.YESU):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 1, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 4, value)


    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_yesu.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.YESU[index]
        self.dao.filter_year_suffix(s[0],s[1])
        self.files_yesu.display()
        #self.files.setSortingEnabled(True)


class Tab_SUYEMO(QWidget):
    def __init__(self, dao, parent=None):
        super(Tab_SUYEMO, self).__init__(parent)
         # year month anzeigen ...
        self.dao = dao
         # years suffix anzeigen


        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        self.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.table = QTableWidget()
        self.table.itemClicked.connect(self.on_kpi_clicked)
        split.addWidget(self.table)

        self.files_suyemo = Files(self.dao)
        split.addWidget( self.files_suyemo)

        self.table.setSortingEnabled(True)
        self.table.setColumnCount(30)
        self.table.setRowCount(len(self.dao.SUYEMO))
        self.table.setHorizontalHeaderLabels([ 'suffix', 'year', 'month','# file', '# directory', '# size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 3
        CNTDIR  = 4
        CNTSIZE = 5


        # suffix years month anzeigen

        for i,s in enumerate(self.dao.SUYEMO):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 1, value)
          value = QTableWidgetItem(s[2])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 2, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 4, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 5, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_suyemo.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.SUYEMO[index]
        self.dao.filter_suffix_year_month(s[0],s[1],s[2])
        self.files_suyemo.display()
        #self.files.setSortingEnabled(True)

class Tab_YEMOSU(QWidget):
    def __init__(self, dao, parent=None):
        super(Tab_YEMOSU, self).__init__(parent)
         # year month anzeigen ...
        self.dao = dao
         # years suffix anzeigen
         # years month suffix anzeigen

        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        self.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.table = QTableWidget()
        self.table.itemClicked.connect(self.on_kpi_clicked)
        split.addWidget(self.table)

        self.files_yemosu = Files(self.dao)
        split.addWidget( self.files_yemosu)


        self.table.setSortingEnabled(True)
        self.table.setColumnCount(30)
        self.table.setRowCount(len(self.dao.YEMOSU))
        self.table.setHorizontalHeaderLabels([ 'year', 'month','suffix','# file', '# directory', '# size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 3
        CNTDIR  = 4
        CNTSIZE = 5


        for i,s in enumerate(self.dao.YEMOSU):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 1, value)
          value = QTableWidgetItem(s[2])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 2, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 4, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 5, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_yemosu.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.YEMOSU[index]
        self.dao.filter_year_month_suffix(s[0],s[1],s[2])
        self.files_yemosu.display()
        #self.files.setSortingEnabled(True)


class Tab_LE(QWidget):
    def __init__(self, dao, parent=None):
        super(Tab_LE, self).__init__(parent)
         # year month anzeigen ...
        self.dao = dao
         # years suffix anzeigen
         # years month suffix anzeigen

    # years month suffix anzeigen


        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        self.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.table = QTableWidget()
        self.table.itemClicked.connect(self.on_kpi_clicked)
        split.addWidget(self.table)

        self.files_le = Files(self.dao)
        split.addWidget( self.files_le)

        self.table.setSortingEnabled(True)
        self.table.setColumnCount(30)
        self.table.setRowCount(len(self.dao.LE))
        self.table.setHorizontalHeaderLabels([ 'level','# file', '# directory', '# size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3


        for i,s in enumerate(self.dao.LE):
          value=QTItem(frmt(str(s[0])),s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 1, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 3, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_le.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.LE[index]
        self.dao.filter_level(s[0])
        self.files_le.display()
        #self.files.setSortingEnabled(True)



class Matrix(QTabWidget):

    def __init__(self, dao, parent=None):
        super(Matrix, self).__init__(parent)
        self.dao = dao

        self.tab_all = Tab_All( dao )
        self.addTab(self.tab_all,'all')
        self.tab_su = Tab_SU( dao )
        self.addTab(self.tab_su,'suffix')
        self.tab_ye = Tab_YE( dao )
        self.addTab(self.tab_ye,'year')
        self.tab_yemo = Tab_YEMO( dao )
        self.addTab(self.tab_yemo,'year month')
        self.tab_suye = Tab_SUYE( dao )
        self.addTab(self.tab_suye,'suffix year')
        self.tab_yesu = Tab_YESU( dao )
        self.addTab(self.tab_yesu,'year suffix')
        self.tab_suyemo= Tab_SUYEMO( dao )
        self.addTab(self.tab_suyemo,'suffix year month')
        self.tab_yemosu= Tab_YEMOSU( dao )
        self.addTab(self.tab_yemosu,'year month suffix')
        self.tab_le= Tab_LE( dao )
        self.addTab(self.tab_le,'level')






class Files(QTableWidget):
    def __init__(self, dao, parent=None):
          super(Files, self).__init__(parent)
          self.dao = dao
          self.itemClicked.connect(self.on_file_clicked)


    def display(self):

        self.setColumnCount(9)
        self.setRowCount(len(self.dao.FIL))
        self.clear()
        self.clearContents()
        #self.hide()
        print('clickBegin', len(self.dao.FIL))
        for i, fil in enumerate(self.dao.FIL):
          row=self.dao.A[fil]
          value = QTableWidgetItem(row[SUFFIX])
          value.setText(row[SUFFIX])
          self.setItem(i, 0, value) # spalte suffix
          value = QTableWidgetItem(row[FILE])
          value.setBackground(BRUSH_FILE)
          self.setItem(i, 1, value) # spalte file
          value = QTableWidgetItem(row[NAME])
          value.setData(5,fil)   # bei filename wird intern auch file gespeichert zwecks Positionierung in nemo
          value.setBackground(BRUSH_FILE)
          self.setItem(i, 2, value) # spalte filename
          value = QTableWidgetItem(str(row[DIRECTORY]))
          value.setData(5,fil)   # beim Directory wird intern auch file gespeichert zwecks Positionierung in nemo
          value.setBackground(BRUSH_DIRECTORY)
          self.setItem(i, 3, value) # spalte directory


          value = QTableWidgetItem(row[YEAR])
          self.setItem(i, 4, value)
          value = QTableWidgetItem(row[MONTH])
          self.setItem(i, 5, value)

          value = QTableWidgetItem(row[TIMESTAMP])
          self.setItem(i, 6, value)

          value = QTItem(frmt(row[LEVEL]), int(row[LEVEL]))
          value.setTextAlignment(Qt.AlignRight)
          self.setItem(i, 7, value)

          value = QTItem(frmt(row[SIZE]), int(row[SIZE]))
          value.setTextAlignment(Qt.AlignRight)
          self.setItem(i, 8, value)


          # Spaltennamen der Filetabelle setzen
        self.setHorizontalHeaderLabels( ['suffix','file', 'name', 'directory', 'year','month','timestamp' , 'level', 'size'])
        print('clickEND')
        self.setSortingEnabled(True)
        # spalte filename vollständig anzeigen ...
        self.resizeColumnToContents(2)
        #self.show()


    def on_file_clicked(self, item):

        index = item.data(5)
        command=''
        if item.column() == 1: # click auf file
          command = 'xdg-open '+'\''+item.text()+'\''
          # das File muss in Hochkommata stehen, da der finename ein blank enthalten kann
        if item.column() == 2: # click auf filename
          # Achtung: data enthaelt  filename incl path, damit nemo in dem Directory auf das File positioniert ...
          command = 'xdg-open '+'\''+self.dao.A[index][FILE]+'\''
          # das Directory muss in Hochkommata stehen, da der finename ein blank enthalten kann
        if item.column() == 3: # click auf directory
          # Achtung: data enthaelt  filename incl path, damit nemo in dem Directory auf das File positioniert ...
          command = 'nemo '+'\''+self.dao.A[index][FILE]+'\''

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

        self.matrix = Matrix(daoA)
        split.addWidget(self.matrix)





 # assemble tab 2 ...
        tab2 = QWidget()
        layouttab = QVBoxLayout()   #masterdetaillayout soll nur den Splitter als einzige Komponente beinhalten
        tab2.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        matrix = Matrix(daoB)
        split.addWidget(matrix)








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
            self.daoA.A=self.daoA.dedub()
            self.daoA.count_files()

            self.matrix.tab_all.set_content()
            #self.matrix.tab_all.table.update()

        #if name == "":
            QMessageBox.information( self, "Empty Field",
                                    "Please enter a name and address.")
            return
        #else:
         #   QMessageBox.information(self, "Success!",
          #                          "Hello %s !" % name)










daoA = Dao(DATA_SOURCE_A)
daoA.selection()
daoA.count_files()
daoA.dedub()

daoB = Dao(DATA_SOURCE_B)
daoB.selection()
daoB.count_files()
daoConfig = DaoConfig()
Dao.difference(daoA,daoB)
# A=[3,2,1,7,7]
# B=[3,2,1]
# L,M,R = Dao.diff(A,B)
# print('A=',A,'B=',B)
# print('L=',L,'M=',M,'R=',R)
#daoL,daoM,daoR = Dao.difference(daoA,daoB)
#print('A=', len(daoA.A), 'B=', len(daoB.A), 'L=',len(daoL.A),'M=',len(daoM.A),'R=',len(daoR.A))





#Dao.dedup(daoA)



app = QApplication(sys.argv)
screen = Form( daoA, daoB, daoConfig )
screen.show()



R=daoA.dedub()


sys.exit(app.exec_())











