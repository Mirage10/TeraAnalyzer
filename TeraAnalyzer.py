



# PyQt5 examples: http://nullege.com/codes/show/src%40p%40y%40pyqt5-HEAD%40examples%40sql%40cachedtable.py/46/PyQt5.QtWidgets.QTableView/python
from datetime import date
import itertools as it
import collections as co
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



    def dedup( self ):

        daoDup = Dao()

        # keine Duplikate vorhanden wenn nicht mindestens 2 Eintraege vorhanden sind ...
        if len(self.A) <= 1:
            return
        # Filelaenge in das Feld hash uebertragen ...




        C=[]
        for i, a in enumerate(self.A):
            C.append([i,a[SIZE]])
        C.sort(key=getkey2)


        i=1
        k=0

        while i<len(C):
            if C[i] != C[i-1]:
                i+=1
                continue
            k=i-1
            while k<len(C):
                pass













        for a in self.A:
            a[HASH] = int(a[SIZE])

        # nach size sortieren
        self.A.sort(key=getkeysize)

        for i, a in enumerate(self.A[:-1]):
            b=self.A[i+1]
            if a[SIZE] == b[SIZE]:
                f=open(a[FILE],'rb')
                h=hash(f.read())
                if h < 0: h=-h
                a[HASH] = h

                # Achtung dies koennte effizienter sein, da hash werte doppelt berechnet werden ...
                f=open(b[FILE],'rb')
                h=hash(f.read())
                if h < 0: h=-h
                b[HASH] = h
                #print('duplicaate',b[SIZE],'hash',h)

        # nach hash sortieren
        self.A.sort(key=getkeyhash)

        # duplicate ermitteln und in ein separates dao abspeichern ...
        i=len(self.A)-1
        while i>0:
            a=self.A[i-1]
            b=self.A[i]
            if a[HASH]==b[HASH]:
                daoDup.A.append(b)
                del self.A[i]
            i=i-1
        #print('Duplicate:', len(daoDup.A)+len(self.A))
        s=[]
        for a in self.A:
            s.append(a[HASH])

        # ab hier sind die HASH-Werte in A unique; alle duplicate sind eliminiert ...
        # Achtung in daoDup stehen nicht mehr der Eintrag aus A, zu dem sie duplikat sind ...
        return daoDup

####







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
        self.path = ''
        if datasource == DATA_SOURCE_A or datasource == DATA_SOURCE_B:
            conf = DaoConfig()
            self.path = conf.value_get(datasource,'Please enter a Directory')
            print('ein Path: ',self.path)

    def getkeylen(self,item):
        s=self.A[item][SIZE]
        return s



    def dedub(self):

        self.B=[i for i, a in enumerate(self.A)]
        self.B.sort(key=self.getkeylen)

        R=[]

        flag=False


        for i, b in enumerate(self.B):
            if i==0: continue
            a=self.A[self.B[i-1]]
            b=self.A[b]
            if a==b:
              R.append(self.B[i-1])
              flag=True
              continue
            if flag:
               R.append(self.B[i-1])
               flag=False

        if flag:
        # falls Gleichheit bis ans Ende besteht, den letzten Eintrag noch mitnehmen
            R.append(self.B[-1])
        print('R==',R)



        print('ERGE:  ',[self.A[b][SIZE] for b in self.B])
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
        self.FIL=[ i for i, a in enumerate(self.A) if a[LEVEL] == str(level)]




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
        tab9= self.get_tab_cat_level()
        self.addTab(tab9,'level')



        tab1.itemClicked.connect(self.on_matrixfiles_clicked_all)
        tab2.itemClicked.connect(self.on_matrixfiles_clicked_su)
        tab3.itemClicked.connect(self.on_matrixfiles_clicked_ye)
        tab4.itemClicked.connect(self.on_matrixfiles_clicked_yemo)
        tab5.itemClicked.connect(self.on_matrixfiles_clicked_suye)
        tab6.itemClicked.connect(self.on_matrixfiles_clicked_yesu)
        tab7.itemClicked.connect(self.on_matrixfiles_clicked_suyemo)
        tab8.itemClicked.connect(self.on_matrixfiles_clicked_yemosu)
        tab9.itemClicked.connect(self.on_matrixfiles_clicked_le)






        # self.setSortingEnabled(True)
    def get_tab_cat_all(self):
         # all anzeigen

        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(100)
        table.setHorizontalHeaderLabels(['all', '# file', '# directory','# size'])

        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3

        for i,s in enumerate(self.dao.ALL):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(0, 0, value)
          value = QTItem(str(s[CNTFILE]), s[CNTFILE] )
          # zelle pastell rot ...
          value.setData(5,i) ##########################
          value.setBackground(BRUSH_TARGET)
          table.setItem(0, 1, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(0, 2, value)
          value = QTItem(frmt(s[CNTSIZE]),s[CNTSIZE]  )
          value.setData(5,i) ##########################
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
        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3

        for i,s in enumerate(self.dao.SU):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE]  )
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 1, value)
          value = QTItem(str(s[CNTDIR]), s[CNTDIR]    )
          value.setData(5,i) ##########################
          # zelle pastell rot ...

          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
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

        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3

        table.setHorizontalHeaderLabels([ 'year','# file', '# directory', '# size'])
        for i,s in enumerate(self.dao.YE):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE]        )
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 1, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR]   )
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
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
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4


        for i,s in enumerate(self.dao.YEMO):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(str(s[CNTDIR]), s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...dao.YEMO[k][CNTDIR]
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.files.setSortingEnabled(False)
          table.setItem(i, 4, value)
        return table

    def get_tab_cat_suffix_year(self):
        # suffix years anzeigen
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(len(self.dao.SUYE))
        table.setHorizontalHeaderLabels([ 'suffix', 'year','# file', '# directory', '# size'])

        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4


        for i,s in enumerate(self.dao.SUYE):
          value = QTableWidgetItem(s[0])
          self.files.setSortingEnabled(False)
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
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

        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4

        for i,s in enumerate(self.dao.YESU):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
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

        CNTFILE = 3
        CNTDIR  = 4
        CNTSIZE = 5


        # suffix years month anzeigen

        for i,s in enumerate(self.dao.SUYEMO):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTableWidgetItem(s[2])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 2, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 4, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
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

        CNTFILE = 3
        CNTDIR  = 4
        CNTSIZE = 5


        for i,s in enumerate(self.dao.YEMOSU):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTableWidgetItem(s[1])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 1, value)
          value = QTableWidgetItem(s[2])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 2, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 3, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 4, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          table.setItem(i, 5, value)
        return table

    def get_tab_cat_level(self):
        # years month suffix anzeigen
        table = QTableWidget()
        table.setSortingEnabled(True)
        table.setColumnCount(30)
        table.setRowCount(len(self.dao.LE))
        table.setHorizontalHeaderLabels([ 'level','# file', '# directory', '# size'])

        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3


        for i,s in enumerate(self.dao.LE):
          value=QTItem(frmt(str(s[0])),s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          table.setItem(i, 0, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 1, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          table.setItem(i, 2, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(5,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          table.setItem(i, 3, value)

        return table





    def on_matrixfiles_clicked_all(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.ALL[index]
        self.dao.filter_all()
        self.files.display()
        #self.files.setSortingEnabled(True)

    def on_matrixfiles_clicked_su(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.SU[index]
        self.dao.filter_suffix(s[0])
        self.files.display()
        #self.files.setSortingEnabled(True)

    def on_matrixfiles_clicked_ye(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.YE[index]
        self.dao.filter_year(s[0])
        self.files.display()
        #self.files.setSortingEnabled(True)
    def on_matrixfiles_clicked_yemo(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.YEMO[index]
        self.dao.filter_year_month(s[0],s[1])
        self.files.display()
        #self.files.setSortingEnabled(True)

    def on_matrixfiles_clicked_suye(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.SUYE[index]
        self.dao.filter_suffix_year(s[0],s[1])
        self.files.display()
        #self.files.setSortingEnabled(True)

    def on_matrixfiles_clicked_yesu(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.YESU[index]
        self.dao.filter_year_suffix(s[0],s[1])
        self.files.display()
        #self.files.setSortingEnabled(True)
    def on_matrixfiles_clicked_suyemo(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.SUYEMO[index]
        self.dao.filter_suffix_year_month(s[0],s[1],s[2])
        self.files.display()
        #self.files.setSortingEnabled(True)

    def on_matrixfiles_clicked_yemosu(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.YEMOSU[index]
        self.dao.filter_year_month_suffix(s[0],s[1],s[2])
        self.files.display()
        #self.files.setSortingEnabled(True)

    def on_matrixfiles_clicked_le(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files.setSortingEnabled(False)
        index = item.data(5)
        s = self.dao.LE[index]
        self.dao.filter_level(s[0])
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
print('haooooooooooooooooooooooooooooooooooooooooooooooooooooooooooollo')
print('RR=',R)

sys.exit(app.exec_())











