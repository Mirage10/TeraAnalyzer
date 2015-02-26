

# todo  clicken auf space A->suffix tab-> 81. eintrag xspf => dump ...
# todo in files tab rename dedupgroups by filesize
# todo after reducing erneute Dedup -> dump
# todo hash button in toolbar

# PyQt5 examples: http://nullege.com/codes/show/src%40p%40y%40pyqt5-HEAD%40examples%40sql%40cachedtable.py/46/PyQt5.QtWidgets.QTableView/python
from datetime import date
import itertools as it
#import collections as co
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
DUBGROUP    = 11
WASTE       = 12


ASTERIX     = '*'
NOCLUSTER   = -1
DATCOMP     = 5
RWCNT       = 40
MAXSIZE     = 4000000




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
        n-=1
    return ret



class DaoConfig():
    def __init__(self):
       self.__settings = QSettings('TeraAnalyzer', 'TeraAnalyzer')
    def value_get(self,key, defaultvalue):
        # dies ist ein Kommentar
        return self.__settings.value(key, defaultvalue)

    def value_set(self,key, value):
        self.__settings.setValue(key,value)





class Api():
    def difference(daoa, daob):
         # dient nur als Prototyp ...
        daol       =Dao()
        daom       =Dao()
        daor       =Dao()
        daoab      =Dao()
        daodyaddiff=Dao()
        A = daoa.A[:]     # es darf auf A daoa.A keine Sortierung erfolgen, daher arbeiten auf Kopie
        B = daob.A[:]
        A.sort(key=getkeysize)
        B.sort(key=getkeysize)
        L=[]
        M=[]
        R=[]
        MA=[]
        MB=[]

        lena = len(A)
        lenb = len(B)
        i = 0
        j = 0
        while i<lena and j < lenb:
            a=A[i]
            b=B[j]
            if a[SIZE] < b[SIZE]:
              L.append(a)
              i+=1
              continue
            if a[SIZE] > b[SIZE]:
              R.append(b)
              j+=1
              continue
            if a[SIZE] == b[SIZE]:
              MA.append(a)
              MB.append(b)
              i+=1
              j+=1
              continue

        # Rest aufnehmen, falls fuer i Ende lena nicht erreicht ...
        for p in range(i,lena):
            L.append(A[p])
        # Rest aufnehmen, falls fuer j Ende lenb nicht erreicht ...
        for p in range(j,lenb):
            R.append(B[p])




        # MA und MB enthaelt files mit gleicher Laenge. Hier ist Phase II anzuwenden: Hashcodes ermitteln und dann die Vergleiche auf derselbigen ...
        for a in MA:
            # wird eine bestimmte Groesse ueberschritten, so kann dies als hash-Wert betrachtet werden ...
            if a[SIZE] > MAXSIZE:
                a[HASH]=a[SIZE]
                continue
            # Fehlerbehandlung erforderlich bei fehlender Berechtigung ...
            with open(a[FILE],'rb') as f:
                h = hash(f.read())
                #print(h)
                if h < 0: h=-h
                a[HASH] = h

        for b in MB:
            # wird eine bestimmte Groesse ueberschritten, so kann dies als hash-Wert betrachtet werden ...
            if b[SIZE] > MAXSIZE:
                b[HASH]=b[SIZE]
                continue
            # Fehlerbehandlung erforderlich bei fehlender Berechtigung ...
            with open(b[FILE],'rb') as f:
                h = hash(f.read())
                #print(h)
                if h < 0: h=-h
                b[HASH] = h

        MA.sort(key=getkeyhash)
        MB.sort(key=getkeyhash)

        lena = len(MA)
        lenb = len(MB)
        i = 0
        j = 0
        while i<lena and j < lenb:
            a=MA[i]
            b=MB[j]
            if a[HASH] < b[HASH]:
              L.append(a)
              i+=1
              continue
            if a[HASH] > b[HASH]:
              R.append(b)
              j+=1
              continue
            if a[HASH] == b[HASH]:
              M.append(a)             # File ist in beiden Mengen vorhanden ...
              i+=1
              j+=1
              continue

        # Rest aufnehmen, falls fuer i Ende lena nicht erreicht ...
        for p in range(i,lena):
            L.append(MA[p])
        # Rest aufnehmen, falls fuer j Ende lenb nicht erreicht ...
        for p in range(j,lenb):
            R.append(MB[p])

        daol.A=L[:]
        daom.A=M[:]
        daor.A=R[:]


        assert len(A)+len(B) == len(L)+2*len(M)+len(R)
        print('Gesamtlaenge A+B:',len(A)+len(B))
        print('Gesamtlaenge l+m+r:',len(L)+2*len(M)+len(R))
        for m in M:
            print('Msize: ', m[SIZE])
        print('M: ', M)

        # die Vereinigungsmenge aus A und B berechnen
        daoab.A=L[:]
        daoab.A.extend(M)
        daoab.A.extend(R)

        # die dyadische Differenz aus A und B berechnen ...  (dyadische Differenz = Vereinigungsmenge von A und B minus Schnittmenge)
        daodyaddiff.A=L[:]
        daodyaddiff.A.extend(R)

        print('dyad:',len(daodyaddiff.A)+2*len(M))
        print('ab: ',len(daoab.A))
        return daol, daom, daor, daoab, daodyaddiff


    def count_files(dao, reduc=False):
        if reduc:
          # redundante Eintraege zwischenspeichern ...
          dao.Expand = [a for a in dao.A if a[WASTE]]
          # Redundanzbefreiung ...
          dao.A = [a for a in dao.A if not a[WASTE]]

        else:
          if len(dao.Expand):
              dao.A.extend(dao.Expand)
              dao.Expand=[]


        print('Beginn zaehlen')
        # Achtung: hier wird A sortiert; Die Sortierreihenfolge von A darf wegen Referenzen auf derselbigen nicht veraendert werden ...

        # Summe der Dateigroessen ermitteln ...
        size_all=0
        waste = 0
        for a in dao.A:
            size_all+=int(a[SIZE])
            if a[WASTE]: waste+=int(a[SIZE])


        dao.ALL=[]
        dao.ALL.append((ASTERIX ,len(dao.A), len({a[DIRECTORY]for a in dao.A}),
                                  len({a[DUBGROUP] for a in dao.A  if a[DUBGROUP] >= 1}  ) , len([a[DUBGROUP] for a in dao.A  if a[DUBGROUP] >= 1]   )    , size_all, waste))


        dao.SU = []
        dao.A.sort(key=getkeysuffix)

        for k, F in it.groupby(dao.A, getkeysuffix):
            F=list(F)
            wastesuff = 0
            for f in F:
             if f[WASTE]: wastesuff+=int(f[SIZE])


            dao.SU.append((k , len(F), len({a[DIRECTORY] for a in F }),
                            len({a[DUBGROUP] for a in F  if a[DUBGROUP] >= 1 and a[SUFFIX] == k }  ),
                            len([a[DUBGROUP] for a in F  if a[DUBGROUP] >= 1 and a[SUFFIX] == k ]  ),
                            sum([int(a[SIZE]) for a in F ]),
                            wastesuff
                            ))



        dao.YE = []
        dao.A.sort(key=getkeyyear)
        for k, F in it.groupby(dao.A, getkeyyear):
            F=list(F)
            dao.YE.append((k,len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

        dao.SUYE = []

        dao.A.sort(key=getkeysuffixyear)
        for k, F in it.groupby(dao.A, getkeysuffixyear):
            F=list(F)
            dao.SUYE.append((k[0],k[1],len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

        dao.YESU = []
        dao.A.sort(key=getkeyyearsuffix)
        for k, F in it.groupby(dao.A, getkeyyearsuffix):
            F=list(F)
            dao.YESU.append((k[0],k[1],len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

        dao.YEMO = []
        dao.A.sort(key=getkeyyearmonth)
        for k, F in it.groupby(dao.A, getkeyyearmonth):
            F=list(F)
            dao.YEMO.append((k[0],k[1], len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

        dao.SUYEMO = []
        dao.A.sort(key=getkeysuffixyearmonth)
        for k, F in it.groupby(dao.A, getkeysuffixyearmonth):
            F=list(F)
            dao.SUYEMO.append((k[0],k[1],k[2],len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))


        dao.YEMOSU = []
        dao.A.sort(key=getkeyyearmonthsuffix)
        for k, F in it.groupby(dao.A, getkeyyearmonthsuffix):
            F=list(F)
            dao.YEMOSU.append(( k[0],k[1],k[2], len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))


        dao.LE = []
        dao.A.sort(key=getkeylevel)
        for k, F in it.groupby(dao.A, getkeylevel):
            F=list(F)
            dao.LE.append((k , len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))


        print('Ende Zählen')
        print('Das Ergebnis')



    def selection(dao):
          print('Beginn Selektion')
          dao.A=[]
          for root, Dir, File in os.walk(dao.path):
            for file in File:
              if file[0] == '.': continue
              a = os.path.join(root, file)
              if '/.' in os.path.join(root, a): continue
              if SUFFIXES and os.path.splitext(a)[1].lower() not in SUFFIXES: continue
              if not os.path.exists(a): continue
              dao.A.append( [ str(a),
                               str(os.path.dirname(a)),
                               str(os.path.basename(a)),
                               str(os.path.splitext(a)[1][1:].lower()),
                               str(os.stat(a).st_mtime),
                               str(date.fromtimestamp(os.stat(a).st_mtime).year),
                               str('0'+str(date.fromtimestamp(os.stat(a).st_mtime).month))[-2:],
                               str(date.fromtimestamp(os.stat(a).st_mtime).year)+' '+str(date.fromtimestamp(os.stat(a).st_mtime).month),
                               os.stat(a).st_size,
                               a.count('/')-1,  #level
                               0,               #hash
                               NOCLUSTER,       #duplicate cluster, default = -1
                               0] )             #duplicate   (as waste)  originaleintrag bleibt erhalten und ist ein duplicate


          print('Ende Selektion')

    def filter_all(dao):
        dao.FIL=[ i for i, a in enumerate (dao.A)]

    def filter_suffix(dao,suffix):
        dao.FIL=[ i for i, a in enumerate(dao.A) if a[SUFFIX] == suffix]
    def filter_year(dao,year):
        dao.FIL=[ i for i, a in enumerate(dao.A) if a[YEAR] == year]
    def filter_year_month(dao,year,month):
        dao.FIL=[ i for i, a in enumerate(dao.A) if a[YEAR] == year and a[MONTH] == month  ]
    def filter_suffix_year(dao,suffix,year):
        dao.FIL=[ i for i, a in enumerate(dao.A) if a[SUFFIX] == suffix and a[YEAR] == year  ]
    def filter_year_suffix(dao,year, suffix):
        dao.FIL=[ i for i, a in enumerate(dao.A) if a[YEAR] == year and a[SUFFIX] == suffix  ]
    def filter_suffix_year_month(dao, suffix, year, month):
        dao.FIL=[ i for i, a in enumerate(dao.A) if a[SUFFIX] == suffix and a[YEAR] == year and a[MONTH] == month  ]
    def filter_year_month_suffix(dao, year, month, suffix):
        dao.FIL=[ i for i, a in enumerate(dao.A) if a[YEAR] == year and a[MONTH] == month and a[SUFFIX] == suffix  ]
    def filter_level(dao,level):
        dao.FIL=[ i for i, a in enumerate(dao.A) if a[LEVEL] == level]


    def dedub(dao):

        # Achtung: Auf A keine Sortierung machen. Alle Pointer erwarten die anfangs gemachte Reihenfolge ...
        # Achtung Nebeneffekt: Dedub setzt die dedubgroup in A ...


        B=[i for i, a in enumerate(dao.A)]
        B.sort(key=dao.getkeylen)
        # in R sollen die pointer auf A stehen, die die gleichen Längen haben...
        R=[]


        flag=False

        # Gruppenstufenermittlung: Elemente mit die zu einer gleichbleibenden Seqzenz gehoeren in R aufnehmen ...
        for i, b in enumerate(B):
            if i==0: continue
            x=dao.A[B[i-1]][SIZE]
            y=dao.A[b][SIZE]
            if x==y:
              R.append(B[i-1])
              flag=True
              continue

            if flag:
               R.append(B[i-1])
               flag=False

        if flag:
        # falls Gleichheit bis ans Ende besteht, den letzten Eintrag noch mitnehmen
            R.append(B[-1])

        # In R stehen Elemente mit gleichen Sequenzen; schon zu Beginn gibt es mindestens 2 gleiche aufeinanderfolgende Elemente ...


        # hash werte fuer genau die Elemente in R berechnen. Hash werte werden auf Ebene von A gespeichert...
        for r in R:
            if dao.A[r][SIZE]==0:
                # Files mit Länge 0 bekommen 0 als Hashwert ...
                dao.A[r][HASH] = 0
                continue
            if dao.A[r][SIZE] > MAXSIZE:
                # Achtung Heuristik: hier wird angenommen, dass bei grossen Files die Filelaenge als Hash-Wert fungieren kan; dies ist nicht
                # immer richtig, aber mit hoher Wahrscheinlichkeit. Womoeglich ist diese Option in der Configuration anzubieten ...
                dao.A[r][HASH] = dao.A[r][SIZE]
                continue

            try:

                # Fehlerbehandlung erforderlich bei fehlender Berechtigung ...
                with open(dao.A[r][FILE],'rb') as f:
                    h = hash(f.read())
                    #print(h)
                    if h < 0: h=-h
                    dao.A[r][HASH] = h
                    #print(self.A[r][HASH])
            except:
                pass


        # Phase II: weitere Einschränkung von R ...
        # analog wie oben die duplikatermittlung auf hash, statt auf len ...

        R.sort(key=dao.getkeyhash)
        # in S sollen die pointer auf A stehen, die die gleichen hashes(laengen) haben...
        S=[]

        flag=False


        for i, r in enumerate(R):
            if i==0: continue
            x=dao.A[R[i-1]][HASH]
            y=dao.A[r][HASH]
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
        S.sort(key=dao.getkeylen)


        # duplicate group in A setzen ...
        for s in S: dao.A[s][DUBGROUP] = dao.A[s][HASH]



        # ab hier sollen die dubroups statt hash werte normale integer sein ...
        S.sort(key=dao.getkeydubgroup)



        if len(S)==0: return     # tritt ein beispielsweise nach Reduce+Dedup ...


        if len(dao.A) > 1:
          # Gruppenbildung macht nur Sinn, wenn mindestens 2 Files vorhanden sind ...
          i = 1
          x = dao.A[S[0]][DUBGROUP]
          dao.A[S[0]][DUBGROUP] = 1        # Achtung die Sequenz verweist anfangs auf mindestens zwei gleiche Elemente. Zaehlung beginnt bei 1 ...
          for s in S[1:]:
              y = dao.A[s][DUBGROUP]
              if x==y:
                  dao.A[s][DUBGROUP] = i
                  dao.A[s][WASTE] = 1   # wenn kein Gruppenstufenwechsel, dann liegt waste vor. achtung zu Beginn einer Gruppenstufe ist waste =0 (Originaleintrag)
                  continue
              if x!=y:
                  x=y
                  i+=1

                  dao.A[s][DUBGROUP] = i



        # alle -1 Werrte, d.h. es gibt keine Duplikate, auf 0 setzen...

        for a in dao.A:
            if a[DUBGROUP] == NOCLUSTER: a[DUBGROUP] = 0



        #return R

class Dao():


   def __init__(self, datasource=None):
        self.A=[]
        self.FIL=[]
        self.ALL=[]
        self.SU=[]
        self.YE= []
        self.YEMO=[]
        self.YESU=[]
        self.YEMOSU=[]
        self.SUYEMO=[]
        self.LE=[]
        self.SUYE=[]
        self.Expand=[]

        self.path = ''
        if datasource == DATA_SOURCE_A or datasource == DATA_SOURCE_B:
            conf = DaoConfig()
            self.path = conf.value_get(datasource,'Please enter a Directory')
            print('ein Path: ',self.path)




   def getkeylen(self,item):
        s=self.A[item][SIZE]
        return s



   def getkeydubgroup(self,item):
        s=self.A[item][DUBGROUP]
        return s


   def getkeyhash(self,item):
        s=self.A[item][HASH]
        return s








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
        self.table.setHorizontalHeaderLabels(['all', '# file', '# directory', '# dubfiles', '# dubgroup', 'size','waste'])
        self.set_content()
        #self.set_tab_content_all(tab)
        #tab.xxx=self.set_tab_content_all



    def set_content(self):
        CNTFILE      = 1
        CNTDIR       = 2
        CNTDUPGROUP  = 3
        CNTDUPFILES  = 4
        CNTSIZE      = 5
        CNTWASTE     = 6
        self.table.clear()
        # rows are changing ...
        self.table.setRowCount(len(self.dao.ALL)+RWCNT)

        for i,s in enumerate(self.dao.ALL):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(0, 0, value)
          value = QTItem(str(s[CNTFILE]), s[CNTFILE] )
          # zelle pastell rot ...
          value.setData(DATCOMP,i) ##########################
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(0, 1, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(0, 2, value)

          value = QTItem(str(s[CNTDUPFILES]),s[CNTDUPFILES])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(0, 3, value)


          value = QTItem(str(s[CNTDUPGROUP]),s[CNTDUPGROUP])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(0, 4, value)


          value = QTItem(frmt(s[CNTSIZE]),s[CNTSIZE]  )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(0, 5, value)
          value = QTItem(frmt(s[CNTWASTE]),s[CNTWASTE]  )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(0, 6, value)




          #table.setSortingEnabled(True)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_all.setSortingEnabled(False)
        index = item.data(DATCOMP)
        s = self.dao.ALL[index]
        Api.filter_all(self.dao)
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
        self.table.setHorizontalHeaderLabels([ 'suffix','# file', '# directory',  '# dubfiles', '# dubgroup', 'size','waste'])
        self.set_content()

    def set_content(self):
        # suffixe anzeigen ...
        CNTFILE      = 1
        CNTDIR       = 2
        CNTDUPGROUP  = 3
        CNTDUPFILES  = 4
        CNTSIZE      = 5
        CNTWASTE     = 6
        # rows are changing ...
        self.table.clear()
        self.table.setRowCount(len(self.dao.SU)+RWCNT)


        for i,s in enumerate(self.dao.SU):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE] )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 1, value)
          value = QTItem(str(s[CNTDIR]), s[CNTDIR] )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...

          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)

          value = QTItem(str(s[CNTDUPFILES]),s[CNTDUPFILES])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)

          value = QTItem(str(s[CNTDUPGROUP]),s[CNTDUPGROUP])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 4, value)


          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 5, value)

          value = QTItem(frmt(s[CNTWASTE]),s[CNTWASTE]  )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 6, value)



        #table.setSortingEnabled(True)


    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_su.setSortingEnabled(False)
        index = item.data(DATCOMP)
        s = self.dao.SU[index]
        Api.filter_suffix(self.dao,s[0])
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
        self.set_content()

    def set_content(self):
        # years anzeigen
        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3
        self.table.clear()
        # rows are changing ...
        self.table.setRowCount(len(self.dao.YE)+RWCNT)

        self.table.setHorizontalHeaderLabels([ 'year','# file', '# directory', 'size'])
        for i,s in enumerate(self.dao.YE):
          value = QTableWidgetItem(s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE]        )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 1, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR]   )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 3, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_ye.setSortingEnabled(False)
        index = item.data(DATCOMP)
        s = self.dao.YE[index]
        Api.filter_year(self.dao,s[0])
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

        self.table.setHorizontalHeaderLabels([ 'year', 'month','# file', '# directory', 'size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4

        self.table.clear()
        # rows are changing ...
        self.table.setRowCount(len(self.dao.YEMO)+RWCNT)

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
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(str(s[CNTDIR]), s[CNTDIR])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...dao.YEMO[k][CNTDIR]
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)

          self.table.setItem(i, 4, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_yemo.setSortingEnabled(False)
        index = item.data(DATCOMP)
        s = self.dao.YEMO[index]
        Api.filter_year_month(self.dao,s[0],s[1])
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
        self.table.setHorizontalHeaderLabels([ 'suffix', 'year','# file', '# directory', 'size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4

        self.table.clear()
        # rows are changing ...
        self.table.setRowCount(len(self.dao.SUYE)+RWCNT)

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
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 4, value)


    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_suye.setSortingEnabled(False)
        index = item.data(DATCOMP)
        s = self.dao.SUYE[index]
        Api.filter_suffix_year(self.dao,s[0],s[1])
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
        self.table.setHorizontalHeaderLabels([ 'year', 'suffix','# file', '# directory', '# size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4

        self.table.clear()
        # rows are changing ...
        self.table.setRowCount(len(self.dao.YESU)+RWCNT)

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
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 4, value)


    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_yesu.setSortingEnabled(False)
        index = item.data(DATCOMP)
        s = self.dao.YESU[index]
        Api.filter_year_suffix(self.dao,s[0],s[1])
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
        self.table.setHorizontalHeaderLabels([ 'suffix', 'year', 'month','# file', '# directory', 'size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 3
        CNTDIR  = 4
        CNTSIZE = 5

        self.table.clear()
        # suffix years month anzeigen

        # rows are changing ...
        self.table.setRowCount(len(self.dao.SUYEMO)+RWCNT)

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
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 4, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 5, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_suyemo.setSortingEnabled(False)
        index = item.data(DATCOMP)
        s = self.dao.SUYEMO[index]
        Api.filter_suffix_year_month(self.dao,s[0],s[1],s[2])
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
        self.table.setHorizontalHeaderLabels([ 'year', 'month','suffix','# file', '# directory', 'size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 3
        CNTDIR  = 4
        CNTSIZE = 5

        self.table.clear()
        # rows are changing ...
        self.table.setRowCount(len(self.dao.YEMOSU)+RWCNT)

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
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 3, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 4, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 5, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_yemosu.setSortingEnabled(False)
        index = item.data(DATCOMP)
        s = self.dao.YEMOSU[index]
        Api.filter_year_month_suffix(self.dao,s[0],s[1],s[2])
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
        self.table.setHorizontalHeaderLabels([ 'level','# file', '# directory', 'size'])
        self.set_content()

    def set_content(self):
        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3

        self.table.clear()
        # rows are changing ...
        self.table.setRowCount(len(self.dao.LE)+RWCNT)

        for i,s in enumerate(self.dao.LE):
          value=QTItem(frmt(str(s[0])),s[0])
          # zelle hell violett ...
          value.setBackground(BRUSH_COMBI)
          self.table.setItem(i, 0, value)
          value = QTItem(str(s[CNTFILE]),s[CNTFILE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 1, value)
          value = QTItem(str(s[CNTDIR]),s[CNTDIR])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_TARGET)
          self.table.setItem(i, 2, value)
          value = QTItem(frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 3, value)

    def on_kpi_clicked(self,item):
        # es muss erst die Sortierung ausgeschaltet werden, danach kann das Datenauffuellen erfolgen ...
        self.files_le.setSortingEnabled(False)
        index = item.data(DATCOMP)
        s = self.dao.LE[index]
        Api.filter_level(self.dao,s[0])
        self.files_le.display()
        #self.files.setSortingEnabled(True)



class Matrix(QTabWidget):

    def __init__(self, dao, parent=None):
        super(Matrix, self).__init__(parent)
        self.dao = dao
        self.tab_all = Tab_All( self.dao )
        self.addTab(self.tab_all,'all')
        self.tab_su = Tab_SU( self.dao )
        self.addTab(self.tab_su,'suffix')
        self.tab_ye = Tab_YE( self.dao )
        self.addTab(self.tab_ye,'year')
        self.tab_yemo = Tab_YEMO( self.dao )
        self.addTab(self.tab_yemo,'year month')
        self.tab_suye = Tab_SUYE( self.dao )
        self.addTab(self.tab_suye,'suffix year')
        self.tab_yesu = Tab_YESU( self.dao )
        self.addTab(self.tab_yesu,'year suffix')
        self.tab_suyemo= Tab_SUYEMO( self.dao )
        self.addTab(self.tab_suyemo,'suffix year month')
        self.tab_yemosu= Tab_YEMOSU( self.dao )
        self.addTab(self.tab_yemosu,'year month suffix')
        self.tab_le= Tab_LE( self.dao )
        self.addTab(self.tab_le,'level')

    def display(self):
        # update the tabs with fresh data ...
        self.tab_all.set_content()
        self.tab_su.set_content()
        self.tab_ye.set_content()
        self.tab_yemo.set_content()
        self.tab_suye.set_content()
        self.tab_yesu.set_content()
        self.tab_suyemo.set_content()
        self.tab_yemosu.set_content()
        self.tab_le.set_content()

class Files(QTableWidget):
    def __init__(self, dao, parent=None):
          super(Files, self).__init__(parent)
          self.dao = dao
          self.itemClicked.connect(self.on_file_clicked)


    def display(self):

        self.setColumnCount(10)
        self.setRowCount(len(self.dao.FIL))
        self.clear()
        self.clearContents()
        #self.hide()
        print('clickBegin', len(self.dao.FIL))
        # Zeilen Aendern sich ...
        self.setRowCount(len(self.dao.FIL))

        for i, fil in enumerate(self.dao.FIL):
          row=self.dao.A[fil]
          value = QTableWidgetItem(row[SUFFIX])
          value.setText(row[SUFFIX])
          self.setItem(i, 0, value) # spalte suffix
          value = QTableWidgetItem(row[FILE])
          value.setBackground(BRUSH_FILE)
          self.setItem(i, 1, value) # spalte file
          value = QTableWidgetItem(row[NAME])
          value.setData(DATCOMP,fil)   # bei filename wird intern auch file gespeichert zwecks Positionierung in nemo
          value.setBackground(BRUSH_FILE)
          self.setItem(i, 2, value) # spalte filename
          value = QTableWidgetItem(str(row[DIRECTORY]))
          value.setData(DATCOMP,fil)   # beim Directory wird intern auch file gespeichert zwecks Positionierung in nemo
          value.setBackground(BRUSH_DIRECTORY)
          self.setItem(i, 3, value) # spalte directory


          value = QTableWidgetItem(row[YEAR])
          self.setItem(i, 4, value)
          value = QTableWidgetItem(row[MONTH])
          self.setItem(i, 5, value)

          value = QTableWidgetItem(row[TIMESTAMP])
          self.setItem(i, 6, value)

          value = QTItem(str(row[LEVEL]), row[LEVEL])
          value.setTextAlignment(Qt.AlignRight)
          self.setItem(i, 7, value)

          #value = QTableWidgetItem(row[DUBGROUP])
          if row[DUBGROUP] == 0:
              stri = ''
          else:
              stri = str(row[DUBGROUP])
          value = QTItem(stri, row[DUBGROUP])
          value.setTextAlignment(Qt.AlignRight)
          self.setItem(i, 8, value)

          value = QTItem(frmt(row[SIZE]), row[SIZE])
          value.setTextAlignment(Qt.AlignRight)
          self.setItem(i, 9, value)


        # Spaltennamen der Filetabelle setzen
        self.setHorizontalHeaderLabels( ['suffix','file', 'name', 'directory', 'year','month','timestamp' , 'level', 'dubgroup' ,'size'])
        print('clickEND')
        self.setSortingEnabled(True)
        # spalte filename vollständig anzeigen ...
        self.resizeColumnToContents(2)
        #self.show()


    def on_file_clicked(self, item):

        index = item.data(DATCOMP)
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



# assemble tab space A ...
        tab_spaceA = QWidget()
        layouttab = QVBoxLayout()
        tab_spaceA.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente

        self.matrixA = Matrix(daoA)
        split.addWidget(self.matrixA)



 # assemble tab space B ...
        tab_spaceB = QWidget()
        layouttab = QVBoxLayout()
        tab_spaceB.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente


        self.matrixB = Matrix(daoB)
        split.addWidget(self.matrixB)


# assemble tab space Config ...
        tab_spaceConfig = QWidget()
        layouttab3 = QFormLayout()
        tab_spaceConfig.setLayout(layouttab3)


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

        self.matrixA.display()
        self.matrixB.display()










# assemble topwidget ...

#        Menue
#        menu_bar = QMenuBar()
#        operations = menu_bar.addMenu("&Operations")
#        help       = menu_bar.addMenu("&Help")
#
#
        action_Indexing       = QAction('Indexing', self)
        action_DedupSpace     = QAction('Dedup', self)
        action_reduce         = QAction('Reduce', self)
        action_expand         = QAction('Expand', self)
        action_trash          = QAction('Calculate', self)
        action_advanced       = QAction('Advanced', self)
        action_Indexing.triggered.connect(self.submitIndexing)
        action_DedupSpace.triggered.connect(self.submitDedupSapce)

        action_reduce.triggered.connect(self.submitReduce)
        action_expand.triggered.connect(self.submitExpand)
        action_advanced.triggered.connect(self.submitAdvanced)


#       operations.addAction(action_DedupSpace)
#       operations.addAction(action_indexing)
#       operations.addAction(action_reduceB)
#       operations.addAction(action_trash)



        toolbar = QToolBar()
        toolbar.addAction(action_Indexing)
        toolbar.addAction(action_DedupSpace)
        toolbar.addAction(action_reduce)
        toolbar.addAction(action_expand)
        toolbar.addAction(action_trash)
        toolbar.addAction(action_advanced)


        self.tabwid = QTabWidget()


        self.tabwid.addTab(tab_spaceA,'Space A')
        self.tabwid.addTab(tab_spaceB,'Space B')
        self.tabwid.addTab(tab_spaceConfig,'Config')


        toplayout = QVBoxLayout(self)
        toplayout.addWidget(toolbar)
        toplayout.addWidget(self.tabwid)


#       self.matrix.itemClicked.connect(self.on_matrixfiles_clicked)
#       self.files.itemClicked.connect(self.on_file_clicked)
        self.setWindowTitle("Tera-Analyzer")


    def add_CalculationTabs(self,daol,daom,daor,daoab,daodyaddiff):

        # assemble tab space A ...
        tab_spaceAminusB = QWidget()
        layouttab = QVBoxLayout()
        tab_spaceAminusB.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente

        self.matrixAminusB = Matrix(daol)
        split.addWidget(self.matrixAminusB)

        self.tabwid.insertTab(2,tab_spaceAminusB,'Space A - B')


        tab_spaceAintersectB = QWidget()
        layouttab = QVBoxLayout()
        tab_spaceAintersectB.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente

        self.matrixAintersectB = Matrix(daom)
        split.addWidget(self.matrixAintersectB)

        self.tabwid.insertTab(3,tab_spaceAintersectB,'Space A /\ B')


        tab_spaceBminusA = QWidget()
        layouttab = QVBoxLayout()
        tab_spaceBminusA.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente

        self.matrixBminusA = Matrix(daor)
        split.addWidget(self.matrixBminusA)

        self.tabwid.insertTab(4,tab_spaceBminusA,'Space B - A')

        tab_spaceAplusB = QWidget()
        layouttab = QVBoxLayout()
        tab_spaceAplusB.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente

        self.matrixAplusB = Matrix(daoab)
        split.addWidget(self.matrixAplusB)

        self.tabwid.insertTab(5,tab_spaceAplusB,'Space A + B')



        tab_spaceDyadDiff = QWidget()
        layouttab = QVBoxLayout()
        tab_spaceDyadDiff.setLayout(layouttab)

        split = QSplitter()
        split.setOrientation( Qt.Vertical )
        layouttab.addWidget(split) # split als einzige Komponente

        self.matrixDyadDiff = Matrix(daodyaddiff)
        split.addWidget(self.matrixDyadDiff)

        self.tabwid.insertTab(6,tab_spaceDyadDiff,'Space A - B \/ B - A')










    def on_button_clickedA(self):
        ss = QFileDialog(self,"Bitte Directory auswaehlen","/home/user").getExistingDirectory(self)
        if ss:
          self.editA.setText(ss)
          self.daoConfig.value_set('sourceA',ss)
          # Tabs der Matrix von SpaceA werden neu aufgebaut ...
          self.daoA.path = ss
          #self.daoA.selection()
          #self.daoA.count_files()
          #self.matrixA.tab_all.set_content()

    def on_button_clickedB(self):
        ss = QFileDialog(self,'Bitte Directory auswaehlen','/home/user').getExistingDirectory(self)
        if ss:
          self.editB.setText(ss)
          self.daoConfig.value_set('sourceB',ss)
          # Tabs der Matrix von SpaceB werden neu aufgebaut ...
          self.daoB.path = ss



    def submitIndexing(self):
        Api.selection(daoA)
        Api.count_files(self.daoA)
        self.matrixA.display()

        Api.selection(daoB)
        Api.count_files(self.daoB)
        self.matrixB.display()
        print('hallo')

    def submitDedupSapce(self):
            print('Begin Dedup A ')
            Api.dedub(self.daoA)
            Api.count_files(self.daoA)
            self.matrixA.display()
            print('End Dedup A')
            print('Begin Dedup B')
            Api.dedub(self.daoB)
            Api.count_files(self.daoB)
            self.matrixB.display()
            print('End Dedup B')



    def submitReduce(self):

            print('Begin Reduce A ')
            Api.count_files(self.daoA,True)
            self.matrixA.display()
            print('End Reduce A')
            print('Begin Reduce B')
            Api.count_files(self.daoB,True)
            self.matrixB.display()
            print('End Reduce B')

    def submitExpand(self):
            print('Begin Expand A ')
            Api.count_files(self.daoA,False)
            self.matrixA.display()
            print('End Expand A')
            print('Begin Expand B')
            Api.count_files(self.daoB,False)
            self.matrixB.display()
            print('End Expand B')

    def submitAdvanced(self):
            print('Begin Advanced ')
            daol, daom, daor, daoab, daodydiff = Api.difference(self.daoA, self.daoB)

            Api.count_files(daol,False)
            Api.count_files(daom,False)
            Api.count_files(daor,False)
            Api.count_files(daoab,False)
            Api.count_files(daodydiff,False)

            self.add_CalculationTabs(daol, daom, daor, daoab, daodydiff)
            self.matrixAminusB.display()
            self.matrixAintersectB.display()
            self.matrixBminusA.display()
            self.matrixAplusB.display()
            self.matrixDyadDiff.display()


            print('Ende Advanced ')
        #if name == "":
            #QMessageBox.information( self, "Empty Field",
            #                        "Please enter a name and address.")











daoA = Dao(DATA_SOURCE_A)
daoB = Dao(DATA_SOURCE_B)
daoConfig = DaoConfig()



app = QApplication(sys.argv)
screen = Form( daoA, daoB, daoConfig )
screen.show()


sys.exit(app.exec_())











