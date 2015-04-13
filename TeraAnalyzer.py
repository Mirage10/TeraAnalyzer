# todo: recording: statt seriell parallele gnome terminals moeglich? + ggf. aus File single click auf recording entfernen
# todo: menueeintaege alle anzeigen; bei vorhandensein entsprechender filetypen menueeintraege einblenden

# todo: Ordnung bei Selection mit anschliessendem Display
# todo: delete allowed - Security
# todo: Display Music, Documents, Videos, Pictures
# todo: copy + move : fuer unique files sorgen (hash als Unterscheidungsmerkmal)
# todo: Quatratischen Algorithmus fuer Direcories refacturen
# todo: Space A und Space B: mehrere Ordner zulassen, evtl einige ausschliessen, ausschliessen mit einem Minus davor
# todo: in dao.A datum und Uhrzeit als column ergaenzen und in Files anzeigen ...
# todo: in Directory Liste # directories all # #directories subtree einfuegen. evtl noch selected directories jeweils
# todo: in Files: delete and ignore column
# todo: /home   und /hime/user/dropbox   -> in der Schnittmengenbildung B-A und A-B sind Dateien, die dort nicht hingehoeren -> Inkonsistenz
# todo: Logik einbauen: falls hash bereits errechnet, dann nicht nochmal berechnen/ueberschreiben
# todo: in files tab rename dedupgroups by filesize
# todo: hash button in toolbar

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


KPI_FILES     = 'FILES'
KPI_DIRECTORY = 'DIRECTORY'

CONFIG_SOURCEA  = 'sourceA'
CONFIG_SOURCEB  = 'sourceB'
CONFIG_TARGET   = 'target'
CONFIG_ALLOWDEL = 'allowDelete'

class Util():
    @staticmethod
    def getkeysuffix(item):
        return item[SUFFIX]
    @staticmethod
    def getkeyyear(item):
        return item[YEAR]
    @staticmethod
    def getkeysuffixyear(item):
        return item[SUFFIX],item[YEAR]
    @staticmethod
    def getkeyyearsuffix(item):
        return item[YEAR],item[SUFFIX]
    @staticmethod
    def getkeyyearmonth(item):
        return item[YEAR],item[MONTH]
    @staticmethod
    def getkeysuffixyearmonth(item):
        return item[SUFFIX],item[YEAR],item[MONTH]
    @staticmethod
    def getkeyyearmonthsuffix(item):
        return item[YEAR],item[MONTH],item[SUFFIX]
    @staticmethod
    def getkeylevel(item):
        return int(item[LEVEL])
    @staticmethod
    def getkeysize(item):
        return int(item[SIZE])
    @staticmethod
    def getkeyhash(item):
        return item[HASH]



    @staticmethod
    def get_url_stream(file):
        # aus einem xspf-file die http Adresse fuer einen musicstream ermitteln ...
        with open(file,'r') as f:
           text = f.read()
           start= text.find("<location>")       # zwischen <location>http:// ... </location> steht der http stream link
           end  = text.find("</location")
           start+=10                            # das location tag ueberspreingen (10 Zeichen)
           return text[start:end]

    # format with intermediate points for large numbers...
    @staticmethod
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
    @staticmethod
    def selection(dao):
          print('Beginn Selektion')
          dao.A=[]

          conf = DaoConfig()
          text = conf.value_get(dao.datasource,'Please enter a Directory')
          # text nach Pfaden splitten ...
          Entry = text.split('\n')

          Path      = {entry for entry in Entry if len(entry) > 0 and entry[0]=='/'}
          Exclusive = {entry[1:] for entry in Entry if len(entry) > 0 and entry[0]=='-'}




          print(Path)




          for path in Path:
              for root, Dir, File in os.walk(path):
                # root enthält das Directory der Files ...
                for file in File:
                  tobeexcluded = False
                  for excl in Exclusive:
                      a=len(root)
                      b=len(excl)
                      if a >= b:
                          # prüfen, ob root das gleiche Präfix hat wie excl ...
                          if root[0:b]==excl: tobeexcluded = True


                  if tobeexcluded: continue

                  if file[0] == '.': continue
                  a = os.path.join(root, file)
                  if '/.' in os.path.join(root, a): continue
                  if SUFFIXES and os.path.splitext(a)[1].lower() not in SUFFIXES: continue
                  if not os.path.exists(a): continue
                  dao.A.append( [ str(a),
                                   str(os.path.dirname(a)),
                                   str(os.path.basename(a)),
                                   str(os.path.splitext(a)[1][1:].lower()),
                                   int(round(os.stat(a).st_mtime)),
                                   str(date.fromtimestamp(os.stat(a).st_mtime).year),
                                   str('0'+str(date.fromtimestamp(os.stat(a).st_mtime).month))[-2:],
                                   str(date.fromtimestamp(os.stat(a).st_mtime).year)+' '+str(date.fromtimestamp(os.stat(a).st_mtime).month),
                                   os.stat(a).st_size,
                                   a.count('/')-1,  #level
                                   0,               #hash
                                   NOCLUSTER,       #duplicate cluster, default = -1
                                   0] )             #duplicate   (as waste)  originaleintrag bleibt erhalten und ist ein duplicate

              print('Ende Selektion')


    @staticmethod
    def difference(daoa, daob):
         # dient nur als Prototyp ...
        daol       =Dao()
        daom       =Dao()
        daor       =Dao()
        daoab      =Dao()
        daodyaddiff=Dao()
        A = daoa.A[:]     # es darf auf A daoa.A keine Sortierung erfolgen, daher arbeiten auf Kopie
        B = daob.A[:]
        A.sort(key=Util.getkeysize)
        B.sort(key=Util.getkeysize)
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
                if h < 0: h=-h
                b[HASH] = h

        MA.sort(key=Util.getkeyhash)
        MB.sort(key=Util.getkeyhash)

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

    @staticmethod
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
        dao.A.sort(key=Util.getkeysuffix)

        for k, F in it.groupby(dao.A, Util.getkeysuffix):
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
        dao.A.sort(key=Util.getkeyyear)
        for k, F in it.groupby(dao.A, Util.getkeyyear):
            F=list(F)
            dao.YE.append((k,len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

        dao.SUYE = []

        dao.A.sort(key=Util.getkeysuffixyear)
        for k, F in it.groupby(dao.A, Util.getkeysuffixyear):
            F=list(F)
            dao.SUYE.append((k[0],k[1],len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

        dao.YESU = []
        dao.A.sort(key=Util.getkeyyearsuffix)
        for k, F in it.groupby(dao.A, Util.getkeyyearsuffix):
            F=list(F)
            dao.YESU.append((k[0],k[1],len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

        dao.YEMO = []
        dao.A.sort(key=Util.getkeyyearmonth)
        for k, F in it.groupby(dao.A, Util.getkeyyearmonth):
            F=list(F)
            dao.YEMO.append((k[0],k[1], len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))

        dao.SUYEMO = []
        dao.A.sort(key=Util.getkeysuffixyearmonth)
        for k, F in it.groupby(dao.A, Util.getkeysuffixyearmonth):
            F=list(F)
            dao.SUYEMO.append((k[0],k[1],k[2],len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))


        dao.YEMOSU = []
        dao.A.sort(key=Util.getkeyyearmonthsuffix)
        for k, F in it.groupby(dao.A, Util.getkeyyearmonthsuffix):
            F=list(F)
            dao.YEMOSU.append(( k[0],k[1],k[2], len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))


        dao.LE = []
        dao.A.sort(key=Util.getkeylevel)
        for k, F in it.groupby(dao.A, Util.getkeylevel):
            F=list(F)
            dao.LE.append((k , len(F), len({a[DIRECTORY] for a in F }) , sum([int(a[SIZE]) for a in F ])))



        # am Schluss wird A sortiert nach suffix, weil dies die primäre Ansicht in Files ist ...
        dao.A.sort(key=Util.getkeysuffix)

        print('Ende Zählen')
        print('Das Ergebnis')




    @staticmethod
    def filter_all(dao, kpi):
        if kpi == KPI_FILES or KPI_DIRECTORY:
          dao.FIL=[ i for i, a in enumerate (dao.A)]

        if kpi == KPI_DIRECTORY:
            D = list({a[DIRECTORY] for a in dao.A})
            #sorted(D)




            for i,d in enumerate(D):
                length = len(d)
                treecnt             = 0
                treesize            = 0
                treeselectedcnt     = 0   #subtree
                treeselectedsize    = 0  # subtree

                topcnt              = 0
                topsize             = 0
                topselectedcnt      = 0   #toplevel
                topselectedsize     = 0  #toplevel
                subtreecnt          = 0
                subtreesize         = 0
                subtreeselectedcnt  = 0
                subtreeselectedsize = 0
                for a in dao.A:
                    if  a[FILE][:length]==d:
                       treecnt += 1
                       treesize += a[SIZE]
                       if True:
                          treeselectedcnt  += 1
                          treeselectedsize +=a[SIZE]
                    if  a[DIRECTORY]==d:
                       topcnt += 1
                       topsize += a[SIZE]
                       if True:
                          topselectedcnt  += 1
                          topselectedsize +=a[SIZE]
                    if  a[FILE][:length]==d and a[DIRECTORY] != d:
                        # we are in a subdirectory ...
                        if True:
                          subtreeselectedcnt +=1
                          subtreeselectedsize +=a[SIZE]
                        subtreecnt +=1
                        subtreesize +=a[SIZE]




                D[i]=[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]

            dao.DIR = D











    @staticmethod
    def filter_suffix(dao,kpi, suffix):
        if kpi == KPI_FILES or kpi==KPI_DIRECTORY:
          dao.FIL=[ i for i, a in enumerate(dao.A) if a[SUFFIX] == suffix] # nur indices stehen in FIL

        if kpi == KPI_DIRECTORY:
            D = list({a[DIRECTORY] for a in dao.A if a[SUFFIX] == suffix})
            #sorted(D)


            for i,d in enumerate(D):
                length = len(d)


                treecnt             = 0
                treesize            = 0
                treeselectedcnt     = 0   #subtree
                treeselectedsize    = 0  # subtree

                topcnt              = 0
                topsize             = 0
                topselectedcnt      = 0   #toplevel
                topselectedsize     = 0  #toplevel
                subtreecnt          = 0
                subtreesize         = 0
                subtreeselectedcnt  = 0
                subtreeselectedsize = 0


                for a in dao.A:
                    if  a[FILE][:length]==d:
                       treecnt += 1
                       treesize += a[SIZE]
                       if a[SUFFIX] == suffix:
                          treeselectedcnt  += 1
                          treeselectedsize +=a[SIZE]
                    if  a[DIRECTORY]==d:
                       topcnt += 1
                       topsize += a[SIZE]
                       if a[SUFFIX] == suffix:
                          topselectedcnt  += 1
                          topselectedsize +=a[SIZE]
                    if  a[FILE][:length]==d and a[DIRECTORY] != d:
                        # we are in a subdirectory ...
                        if a[SUFFIX] == suffix:
                          subtreeselectedcnt +=1
                          subtreeselectedsize +=a[SIZE]
                        subtreecnt +=1
                        subtreesize +=a[SIZE]





                D[i]=[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]

            dao.DIR = D







    @staticmethod
    def filter_year(dao,kpi,year):
        if kpi == KPI_FILES or kpi==KPI_DIRECTORY:
          dao.FIL=[ i for i, a in enumerate(dao.A) if a[YEAR] == year]
        if kpi==KPI_DIRECTORY:
            D = list({a[DIRECTORY] for a in dao.A if a[YEAR] == year})


            for i,d in enumerate(D):
                length = len(d)

                treecnt             = 0
                treesize            = 0
                treeselectedcnt     = 0   #subtree
                treeselectedsize    = 0  # subtree

                topcnt              = 0
                topsize             = 0
                topselectedcnt      = 0   #toplevel
                topselectedsize     = 0  #toplevel
                subtreecnt          = 0
                subtreesize         = 0
                subtreeselectedcnt  = 0
                subtreeselectedsize = 0


                for a in dao.A:
                    if  a[FILE][:length]==d:
                       treecnt += 1
                       treesize += a[SIZE]
                       if a[YEAR] == year:
                          treeselectedcnt  += 1
                          treeselectedsize +=a[SIZE]
                    if  a[DIRECTORY]==d:
                       topcnt += 1
                       topsize += a[SIZE]
                       if a[YEAR] == year:
                          topselectedcnt  += 1
                          topselectedsize +=a[SIZE]
                    if  a[FILE][:length]==d and a[DIRECTORY] != d:
                        # we are in a subdirectory ...
                        if a[YEAR] == year:
                          subtreeselectedcnt +=1
                          subtreeselectedsize +=a[SIZE]
                        subtreecnt +=1
                        subtreesize +=a[SIZE]


                D[i]=[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]


            dao.DIR = D






    @staticmethod
    def filter_year_month(dao,kpi,year,month):
        if kpi == KPI_FILES or kpi==KPI_DIRECTORY:
          dao.FIL=[ i for i, a in enumerate(dao.A) if a[YEAR] == year and a[MONTH] == month  ]
        if kpi==KPI_DIRECTORY:
            D = list({a[DIRECTORY] for a in dao.A if a[YEAR] == year and a[MONTH] == month})


            for i,d in enumerate(D):
                length = len(d)
                treecnt             = 0
                treesize            = 0
                treeselectedcnt     = 0   #subtree
                treeselectedsize    = 0  # subtree

                topcnt              = 0
                topsize             = 0
                topselectedcnt      = 0   #toplevel
                topselectedsize     = 0  #toplevel
                subtreecnt          = 0
                subtreesize         = 0
                subtreeselectedcnt  = 0
                subtreeselectedsize = 0


                for a in dao.A:
                    if  a[FILE][:length]==d:
                       treecnt += 1
                       treesize += a[SIZE]
                       if a[YEAR] == year and a[MONTH]==month:
                          treeselectedcnt  += 1
                          treeselectedsize +=a[SIZE]
                    if  a[DIRECTORY]==d:
                       topcnt += 1
                       topsize += a[SIZE]
                       if a[YEAR] == year and a[MONTH]==month:
                          topselectedcnt  += 1
                          topselectedsize +=a[SIZE]
                    if  a[FILE][:length]==d and a[DIRECTORY] != d:
                        # we are in a subdirectory ...
                        if a[YEAR] == year and a[MONTH]==month:
                          subtreeselectedcnt +=1
                          subtreeselectedsize +=a[SIZE]
                        subtreecnt +=1
                        subtreesize +=a[SIZE]


                D[i]=[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]


            dao.DIR = D





    @staticmethod
    def filter_suffix_year(dao,kpi,suffix,year):
        if kpi == KPI_FILES or kpi==KPI_DIRECTORY:
          dao.FIL=[ i for i, a in enumerate(dao.A) if a[SUFFIX] == suffix and a[YEAR] == year  ]
        if kpi==KPI_DIRECTORY:
            D = list({a[DIRECTORY] for a in dao.A if a[SUFFIX] == suffix and a[YEAR] == year})

            for i,d in enumerate(D):
                length = len(d)
                treecnt             = 0
                treesize            = 0
                treeselectedcnt     = 0   #subtree
                treeselectedsize    = 0  # subtree

                topcnt              = 0
                topsize             = 0
                topselectedcnt      = 0   #toplevel
                topselectedsize     = 0  #toplevel
                subtreecnt          = 0
                subtreesize         = 0
                subtreeselectedcnt  = 0
                subtreeselectedsize = 0


                for a in dao.A:
                    if  a[FILE][:length]==d:
                       treecnt += 1
                       treesize += a[SIZE]
                       if a[YEAR] == year and a[SUFFIX]==suffix:
                          treeselectedcnt  += 1
                          treeselectedsize +=a[SIZE]
                    if  a[DIRECTORY]==d:
                       topcnt += 1
                       topsize += a[SIZE]
                       if a[YEAR] == year and a[SUFFIX]==suffix:
                          topselectedcnt  += 1
                          topselectedsize +=a[SIZE]
                    if  a[FILE][:length]==d and a[DIRECTORY] != d:
                        # we are in a subdirectory ...
                        if a[YEAR] == year and a[SUFFIX]==suffix:
                          subtreeselectedcnt +=1
                          subtreeselectedsize +=a[SIZE]
                        subtreecnt +=1
                        subtreesize +=a[SIZE]


                D[i]=[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]

            dao.DIR = D




    @staticmethod
    def filter_year_suffix(dao,kpi,year, suffix):
        if kpi == KPI_FILES or kpi==KPI_DIRECTORY:
          dao.FIL=[ i for i, a in enumerate(dao.A) if a[YEAR] == year and a[SUFFIX] == suffix  ]

        if kpi==KPI_DIRECTORY:
            D = list({a[DIRECTORY] for a in dao.A if a[YEAR] == year and a[SUFFIX] == suffix})

            for i,d in enumerate(D):
                length = len(d)
                treecnt             = 0
                treesize            = 0
                treeselectedcnt     = 0   #subtree
                treeselectedsize    = 0  # subtree

                topcnt              = 0
                topsize             = 0
                topselectedcnt      = 0   #toplevel
                topselectedsize     = 0  #toplevel
                subtreecnt          = 0
                subtreesize         = 0
                subtreeselectedcnt  = 0
                subtreeselectedsize = 0


                for a in dao.A:
                    if  a[FILE][:length]==d:
                       treecnt += 1
                       treesize += a[SIZE]
                       if a[YEAR] == year and a[SUFFIX]==suffix:
                          treeselectedcnt  += 1
                          treeselectedsize +=a[SIZE]
                    if  a[DIRECTORY]==d:
                       topcnt += 1
                       topsize += a[SIZE]
                       if a[YEAR] == year and a[SUFFIX]==suffix:
                          topselectedcnt  += 1
                          topselectedsize +=a[SIZE]
                    if  a[FILE][:length]==d and a[DIRECTORY] != d:
                        # we are in a subdirectory ...
                        if a[YEAR] == year and a[SUFFIX]==suffix:
                          subtreeselectedcnt +=1
                          subtreeselectedsize +=a[SIZE]
                        subtreecnt +=1
                        subtreesize +=a[SIZE]


                D[i]=[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]

            dao.DIR = D




    @staticmethod
    def filter_suffix_year_month(dao,kpi, suffix, year, month):
        if kpi == KPI_FILES or kpi==KPI_DIRECTORY:
          dao.FIL=[ i for i, a in enumerate(dao.A) if a[SUFFIX] == suffix and a[YEAR] == year and a[MONTH] == month  ]
        if kpi==KPI_DIRECTORY:
            D = list({a[DIRECTORY] for a in dao.A if a[SUFFIX] == suffix and a[YEAR] == year and a[MONTH] == month})


            for i,d in enumerate(D):
                length = len(d)
                treecnt             = 0
                treesize            = 0
                treeselectedcnt     = 0   #subtree
                treeselectedsize    = 0  # subtree

                topcnt              = 0
                topsize             = 0
                topselectedcnt      = 0   #toplevel
                topselectedsize     = 0  #toplevel
                subtreecnt          = 0
                subtreesize         = 0
                subtreeselectedcnt  = 0
                subtreeselectedsize = 0


                for a in dao.A:
                    if  a[FILE][:length]==d:
                       treecnt += 1
                       treesize += a[SIZE]
                       if a[YEAR] == year and a[SUFFIX]==suffix and a[MONTH]==month:
                          treeselectedcnt  += 1
                          treeselectedsize +=a[SIZE]
                    if  a[DIRECTORY]==d:
                       topcnt += 1
                       topsize += a[SIZE]
                       if a[YEAR] == year and a[SUFFIX]==suffix and a[MONTH]==month:
                          topselectedcnt  += 1
                          topselectedsize +=a[SIZE]
                    if  a[FILE][:length]==d and a[DIRECTORY] != d:
                        # we are in a subdirectory ...
                        if a[YEAR] == year and a[SUFFIX]==suffix and a[MONTH]==month:
                          subtreeselectedcnt +=1
                          subtreeselectedsize +=a[SIZE]
                        subtreecnt +=1
                        subtreesize +=a[SIZE]


                D[i]=[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]


            dao.DIR = D




    @staticmethod
    def filter_year_month_suffix(dao, kpi, year, month, suffix):
        if kpi == KPI_FILES or kpi==KPI_DIRECTORY:
          dao.FIL=[ i for i, a in enumerate(dao.A) if a[YEAR] == year and a[MONTH] == month and a[SUFFIX] == suffix  ]
        if kpi==KPI_DIRECTORY:
            D = list({a[DIRECTORY] for a in dao.A if a[YEAR] == year and a[MONTH] == month and a[SUFFIX] == suffix})

            for i,d in enumerate(D):
                length = len(d)
                treecnt             = 0
                treesize            = 0
                treeselectedcnt     = 0   #subtree
                treeselectedsize    = 0  # subtree

                topcnt              = 0
                topsize             = 0
                topselectedcnt      = 0   #toplevel
                topselectedsize     = 0  #toplevel
                subtreecnt          = 0
                subtreesize         = 0
                subtreeselectedcnt  = 0
                subtreeselectedsize = 0


                for a in dao.A:
                    if  a[FILE][:length]==d:
                       treecnt += 1
                       treesize += a[SIZE]
                       if a[YEAR] == year and a[MONTH]==month and a[SUFFIX]==suffix:
                          treeselectedcnt  += 1
                          treeselectedsize +=a[SIZE]
                    if  a[DIRECTORY]==d:
                       topcnt += 1
                       topsize += a[SIZE]
                       if a[YEAR] == year and a[MONTH]==month and a[SUFFIX]==suffix:
                          topselectedcnt  += 1
                          topselectedsize +=a[SIZE]
                    if  a[FILE][:length]==d and a[DIRECTORY] != d:
                        # we are in a subdirectory ...
                        if a[YEAR] == year and a[MONTH]==month and a[SUFFIX]==suffix:
                          subtreeselectedcnt +=1
                          subtreeselectedsize +=a[SIZE]
                        subtreecnt +=1
                        subtreesize +=a[SIZE]


                D[i]=[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]

            dao.DIR = D


    @staticmethod
    def filter_level(dao,kpi,level):
        if kpi == KPI_FILES or kpi==KPI_DIRECTORY:
          dao.FIL=[ i for i, a in enumerate(dao.A) if a[LEVEL] == level]
        if kpi==KPI_DIRECTORY:
            D = list({a[DIRECTORY] for a in dao.A if a[LEVEL] == level})

            for i,d in enumerate(D):
                length = len(d)
                treecnt             = 0
                treesize            = 0
                treeselectedcnt     = 0   #subtree
                treeselectedsize    = 0  # subtree

                topcnt              = 0
                topsize             = 0
                topselectedcnt      = 0   #toplevel
                topselectedsize     = 0  #toplevel
                subtreecnt          = 0
                subtreesize         = 0
                subtreeselectedcnt  = 0
                subtreeselectedsize = 0


                for a in dao.A:
                    if  a[FILE][:length]==d:
                       treecnt += 1
                       treesize += a[SIZE]
                       if a[LEVEL] == level:
                          treeselectedcnt  += 1
                          treeselectedsize +=a[SIZE]
                    if  a[DIRECTORY]==d:
                       topcnt += 1
                       topsize += a[SIZE]
                       if a[LEVEL] == level:
                          topselectedcnt  += 1
                          topselectedsize +=a[SIZE]
                    if  a[FILE][:length]==d and a[DIRECTORY] != d:
                        # we are in a subdirectory ...
                        if a[LEVEL] == level:
                          subtreeselectedcnt +=1
                          subtreeselectedsize +=a[SIZE]
                        subtreecnt +=1
                        subtreesize +=a[SIZE]


                D[i]=[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]

            dao.DIR = D


    @staticmethod
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
                    if h < 0: h=-h
                    dao.A[r][HASH] = h
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
        self.datasource = datasource





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
BRUSH_FILENAME   = QBrush(QColor(255, 255, 240))  # pastell gelb

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
        self.table.setHorizontalHeaderLabels(['all', '# file', '# directory', '# dubfiles', '# dubgroup', 'size','waste'])
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


          value = QTItem(Util.frmt(s[CNTSIZE]),s[CNTSIZE]  )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(0, 5, value)
          value = QTItem(Util.frmt(s[CNTWASTE]),s[CNTWASTE]  )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(0, 6, value)




    def on_kpi_clicked(self,item):
        index = item.data(DATCOMP)
        s = self.dao.ALL[index]

        if item.column() == 1:
          Api.filter_all(self.dao, KPI_FILES)
          self.files_all.displayFiles()
        if item.column() == 2:
          Api.filter_all(self.dao, KPI_DIRECTORY)
          self.files_all.displayDir()



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
        self.table.setHorizontalHeaderLabels([ 'suffix','# file', '# directory',  '# dubfiles', '# dubgroup', 'size','waste'])

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


          value = QTItem(Util.frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 5, value)

          value = QTItem(Util.frmt(s[CNTWASTE]),s[CNTWASTE]  )
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 6, value)




    def on_kpi_clicked(self,item):
        index = item.data(DATCOMP)
        s = self.dao.SU[index]

        if item.column() == 1:
          Api.filter_suffix(self.dao, KPI_FILES,s[0])
          self.files_su.displayFiles()
        if item.column() == 2:
          Api.filter_suffix(self.dao, KPI_DIRECTORY,s[0])
          self.files_su.displayDir()

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
          value = QTItem(Util.frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 3, value)

    def on_kpi_clicked(self,item):
        index = item.data(DATCOMP)
        s = self.dao.YE[index]

        if item.column() == 1:
          Api.filter_year(self.dao,KPI_FILES,s[0])
          self.files_ye.displayFiles()
        if item.column() == 2:
          Api.filter_year(self.dao,KPI_DIRECTORY,s[0])
          self.files_ye.displayDir()



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


        self.set_content()

    def set_content(self):
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4

        self.table.clear()
        self.table.setHorizontalHeaderLabels([ 'year', 'month','# file', '# directory', 'size'])
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
          value = QTItem(Util.frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)

          self.table.setItem(i, 4, value)

    def on_kpi_clicked(self,item):
        index = item.data(DATCOMP)
        s = self.dao.YEMO[index]

        if item.column() == 2:
          Api.filter_year_month(self.dao,KPI_FILES,s[0],s[1])
          self.files_yemo.displayFiles()
        if item.column() == 3:
          Api.filter_year_month(self.dao,KPI_DIRECTORY,s[0],s[1])
          self.files_yemo.displayDir()



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

        self.set_content()

    def set_content(self):
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4

        self.table.clear()
        self.table.setHorizontalHeaderLabels([ 'suffix', 'year','# file', '# directory', 'size'])
        # rows are changing ...
        self.table.setRowCount(len(self.dao.SUYE)+RWCNT)

        for i,s in enumerate(self.dao.SUYE):
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
          value = QTItem(Util.frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 4, value)


    def on_kpi_clicked(self,item):
        index = item.data(DATCOMP)
        s = self.dao.SUYE[index]

        if item.column() == 2:
          Api.filter_suffix_year(self.dao,KPI_FILES,s[0],s[1])
          self.files_suye.displayFiles()
        if item.column() == 3:
          Api.filter_suffix_year(self.dao,KPI_DIRECTORY,s[0],s[1])
          self.files_suye.displayDir()





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

        self.set_content()

    def set_content(self):
        CNTFILE = 2
        CNTDIR  = 3
        CNTSIZE = 4

        self.table.clear()
        self.table.setHorizontalHeaderLabels([ 'year', 'suffix','# file', '# directory', '# size'])
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
          value = QTItem(Util.frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 4, value)


    def on_kpi_clicked(self,item):
        index = item.data(DATCOMP)
        s = self.dao.YESU[index]

        if item.column() == 2:
          Api.filter_year_suffix(self.dao,KPI_FILES,s[0],s[1])
          self.files_yesu.displayFiles()
        if item.column() == 3:
          Api.filter_year_suffix(self.dao,KPI_DIRECTORY,s[0],s[1])
          self.files_yesu.displayDir()




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

        self.set_content()

    def set_content(self):
        CNTFILE = 3
        CNTDIR  = 4
        CNTSIZE = 5

        self.table.clear()
        self.table.setHorizontalHeaderLabels([ 'suffix', 'year', 'month','# file', '# directory', 'size'])
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
          value = QTItem(Util.frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 5, value)

    def on_kpi_clicked(self,item):
        index = item.data(DATCOMP)
        s = self.dao.SUYEMO[index]

        if item.column() == 3:
          Api.filter_suffix_year_month(self.dao,KPI_FILES,s[0],s[1],s[2])
          self.files_suyemo.displayFiles()
        if item.column() == 4:
          Api.filter_suffix_year_month(self.dao,KPI_DIRECTORY,s[0],s[1],s[2])
          self.files_suyemo.displayDir()



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

        self.set_content()

    def set_content(self):
        CNTFILE = 3
        CNTDIR  = 4
        CNTSIZE = 5

        self.table.clear()
        self.table.setHorizontalHeaderLabels([ 'year', 'month','suffix','# file', '# directory', 'size'])
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
          value = QTItem(Util.frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 5, value)

    def on_kpi_clicked(self,item):
        index = item.data(DATCOMP)
        s = self.dao.YEMOSU[index]

        if item.column() == 3:
          Api.filter_year_month_suffix(self.dao,KPI_FILES,s[0],s[1],s[2])
          self.files_yemosu.displayFiles()
        if item.column() == 4:
          Api.filter_year_month_suffix(self.dao,KPI_DIRECTORY,s[0],s[1],s[2])
          self.files_yemosu.displayDir()




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

        self.set_content()

    def set_content(self):
        CNTFILE = 1
        CNTDIR  = 2
        CNTSIZE = 3

        self.table.clear()
        self.table.setHorizontalHeaderLabels([ 'level','# file', '# directory', 'size'])
        # rows are changing ...
        self.table.setRowCount(len(self.dao.LE)+RWCNT)

        for i,s in enumerate(self.dao.LE):
          value=QTItem(Util.frmt(str(s[0])),s[0])
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
          value = QTItem(Util.frmt(str(s[CNTSIZE])),s[CNTSIZE])
          value.setData(DATCOMP,i) ##########################
          # zelle pastell rot ...
          value.setBackground(BRUSH_SIZE)
          value.setTextAlignment(Qt.AlignRight)
          self.table.setItem(i, 3, value)

    def on_kpi_clicked(self,item):
        index = item.data(DATCOMP)
        s = self.dao.LE[index]

        if item.column() == 1:
          Api.filter_level(self.dao,KPI_FILES,s[0])
          self.files_le.displayFiles()
        if item.column() == 2:
          Api.filter_level(self.dao,KPI_DIRECTORY,s[0])
          self.files_le.displayDir()





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





class ProxyModelFiles(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super(ProxyModelFiles, self).__init__(parent)

    def lessThan(self, left, right):


        col = left.column()

        leftdata  = left.data()
        rightdata = right.data()
        if col == 9:
          # size ...
          leftdata  = int(str(left.data()).replace('.',''))
          rightdata = int(str(right.data()).replace('.',''))
        if col == 6 or col == 7:
          # timestamp, level ...
          leftdata  = int(left.data())
          rightdata = int(right.data())
        if col == 8:
          # dubgroup ...
           if left.data() == '': leftdata = 0    # dedoupgroup ist initial, daher muss die 0 direkt bestimmt werden ...
           else: leftdata = int(left.data())
           if right.data() == '': rightdata = 0
           else: rightdata = int(right.data())

        return leftdata < rightdata

class ProxyModelDir(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super(ProxyModelDir, self).__init__(parent)

    def lessThan(self, left, right):


        col = left.column()

        leftdata  = left.data()
        rightdata = right.data()
        if col == 0:
          # directory...
          leftdata  = str(left.data())
          rightdata = str(right.data())


        return leftdata < rightdata


class Files(QTableView):
    def __init__(self, dao, parent=None):
          super(Files, self).__init__(parent)
          self.dao = dao


          # define context menu ...
          self.setContextMenuPolicy(Qt.CustomContextMenu)
          self.customContextMenuRequested.connect(self.popup)

          self.sortByColumn(0, Qt.AscendingOrder)

          # werden immer beide durchlaufen: sowohl bei displayFiles alsauch bei displayDir ...
          self.clicked.connect(self.on_file_clicked)
          self.clicked.connect(self.on_directory_clicked)   #on_file_clicked





    def onDelete(self):
        # Kopieren der in der Fileuebersicht markierten Files in den Target Ordner ...
        # Namensduplikate werden unique gemacht ...
        print('Beginn Delete')
        selmod = self.selectionModel()
        Fi=[]
        for i in selmod.selection().indexes():
            if i.column()==1:
              Fi.append(self.proxymodel.data(i) )  # column 1 ist das Feld 'File'; die zugehoerige Zelle wird ausgegeben ...
        # uniquefifieren der Dateinamen ...

        for fi in Fi:
          command = 'rm ' + '\'' + fi + '\''
          os.system(command)
        print('Ende Delete')

    def onCopy(self):
        # Kopieren der in der Fileuebersicht markierten Files in den Target Ordner ...
        # Namensduplikate werden unique gemacht ...
        print('Beginn Kopieren')
        config =DaoConfig()
        target = config.value_get(CONFIG_TARGET,'')
        selmod = self.selectionModel()
        Fi=[]
        for i in selmod.selection().indexes():
            if i.column()==1:
              Fi.append(self.proxymodel.data(i) )  # column 1 ist das Feld 'File'; die zugehoerige Zelle wird ausgegeben ...
        # uniquefifieren der Dateinamen ...

        for fi in Fi:
          command = 'cp -p ' + '\'' + fi + '\'' + ' ' + '\'' + target + '\''          #-p: preserve attributes
          os.system(command)
        print('Ende Kopieren')

    def onRecording(self):
        # Recording der in der Fileuebersicht markierten Files ...
        print('Begin Recording')
        selmod = self.selectionModel()
        Fi=[]
        for i in selmod.selection().indexes():
            if i.column()==1:
              Fi.append(self.proxymodel.data(i) )  # column 1 ist das Feld 'File'; die zugehoerige Zelle wird ausgegeben ...

        for fi in Fi:
            if fi.endswith('xspf'):
              #command = 'streamripper http://91.250.77.9:8070 -u gaudi'
              command = 'gnome-terminal --command=\'streamripper ' + Util.get_url_stream(fi) + ' -d /home/user/astreamrip -u gaudi  \''
              os.system(command)
        print('Ende Recording')


    def onMove(self):
        print('Beginn Move')
        config =DaoConfig()
        target = config.value_get(CONFIG_TARGET,'')
        selmod = self.selectionModel()
        Fi=[]
        for i in selmod.selection().indexes():
            if i.column()==1:
              Fi.append(self.proxymodel.data(i) )  # column 1 ist das Feld 'File'; die zugehoerige Zelle wird ausgegeben ...
        # uniquefifieren der Dateinamen ...

        for fi in Fi:
          command = 'mv ' + '\'' + fi + '\'' + ' ' + '\'' + target + '\''
          os.system(command)



        print('Ende Move')
    def onDisplay(self):
        print('Begin Display')

        selmod = self.selectionModel()
        command='eog '     #gnome command: eog=eye of gnome, image viewer
        for i in selmod.selection().indexes():
            if i.column()==1:
              command+= ' \'' +   self.proxymodel.data(i) + '\''  # column 1 ist das Feld 'File'; die zugehoerige Zelle wird ausgegeben ...

        os.system(command)
        print('End Display')
        # wichtig wichtig wichtig
        # find . -type f -name '*.png' -exec eog {} \+

    # pops up the context menu of Files ...
    def popup(self, pos):


        config = DaoConfig()
        allowdel = config.value_get(CONFIG_ALLOWDEL,'')

        menu = QMenu()
        copyAction = menu.addAction("Copy")
        moveAction = menu.addAction("Move")
        deleteAction = menu.addAction("Delete")
        displayAction = menu.addAction('Display')
        recordingAction = menu.addAction('Recording')


        copyAction.triggered.connect(self.onCopy)
        moveAction.triggered.connect(self.onMove)
        deleteAction.triggered.connect(self.onDelete)
        displayAction.triggered.connect(self.onDisplay)
        recordingAction.triggered.connect(self.onRecording)

        # delete nur zulassen, wenn dies in der Configuration explizit angegeben ist ...
        if allowdel == 'X':
          deleteAction.setDisabled(False)
        else:
          deleteAction.setDisabled(True)


        action = menu.exec_(QCursor.pos() )











    def displayFiles(self):
        #self.clicked.disconnect(self)
        #self.clicked.connect(self.on_file_clicked)   #on_file_clicked

        self.proxymodel = ProxyModelFiles()
        self.model =  QStandardItemModel(len(self.dao.FIL), 10, self)
        self.proxymodel.setSourceModel(self.model)
        self.proxymodel.setDynamicSortFilter(False)
        self.setModel(self.proxymodel)


        #selection = self.selectionModel()
        #selection.selectionChanged.connect(self.handleSelectionChanged)


        print('clickBegin', len(self.dao.FIL))
        # Zeilen Aendern sich ...


        for i, fil in enumerate(self.dao.FIL):
          row=self.dao.A[fil]
          value = QStandardItem(row[SUFFIX])
          #value.setText(row[SUFFIX])
          self.model.setItem(i, 0, value) # spalte suffix
          value = QStandardItem(row[FILE])
          value.setBackground(BRUSH_FILENAME)
          self.model.setItem(i, 1, value) # spalte file
          value = QStandardItem(row[NAME])
          value.setBackground(BRUSH_FILE)
          self.model.setItem(i, 2, value) # spalte filename
          value = QStandardItem(str(row[DIRECTORY]))
          value.setBackground(BRUSH_DIRECTORY)
          self.model.setItem(i, 3, value) # spalte directory

          value = QStandardItem(row[YEAR])
          self.model.setItem(i, 4, value)
          value = QStandardItem(row[MONTH])
          self.model.setItem(i, 5, value)

          # Achtung: timestamps muessen nach integer sortiert werden und nicht lexikographisch ...
          value = QStandardItem(str(row[TIMESTAMP]))
          value.setTextAlignment(Qt.AlignRight)
          self.model.setItem(i, 6, value)


          value = QStandardItem(str(row[LEVEL]))
          value.setTextAlignment(Qt.AlignRight)
          self.model.setItem(i, 7, value)

          if row[DUBGROUP] == 0:
              stri = ''
          else:
              stri = str(row[DUBGROUP])
          value = QStandardItem(stri)
          value.setTextAlignment(Qt.AlignRight)
          self.model.setItem(i, 8, value)

          value = QStandardItem(Util.frmt(row[SIZE]))
          value.setTextAlignment(Qt.AlignRight)
          self.model.setItem(i, 9, value)


        # Spaltennamen der Filetabelle setzen
        self.model.setHorizontalHeaderLabels( ['suffix','file', 'name', 'directory', 'year','month','timestamp' , 'level', 'dubgroup' ,'size'])
        print('clickEND')
        self.setSortingEnabled(True)
        # spalte filename vollständig anzeigen ...
        self.resizeColumnToContents(2)
        self.resizeColumnToContents(0)


    def displayDir(self):
        #self.clicked.disconnect(self)


        self.proxymodel = ProxyModelDir()
        self.model =  QStandardItemModel(len(self.dao.DIR), 10, self)
        self.proxymodel.setSourceModel(self.model)
        self.proxymodel.setDynamicSortFilter(False)
        self.setModel(self.proxymodel)


        #selection = self.selectionModel()
        #selection.selectionChanged.connect(self.handleSelectionChanged)


        print('clickBegin', len(self.dao.DIR))
        # Zeilen Aendern sich ...

        # d,topselectedcnt, topcnt,  subtreeselectedcnt,subtreecnt, topselectedsize, topsize, subtreeselectedsize , subtreesize ]
        for i, dir in enumerate(self.dao.DIR):

          value = QStandardItem(dir[0])   #directory
          value.setBackground(BRUSH_DIRECTORY)
          self.model.setItem(i, 0, value) #
          value = QStandardItem(str(dir[1]))   #files
          value.setBackground(BRUSH_TARGET)
          self.model.setItem(i, 1, value) #
          value = QStandardItem(str(dir[2]))   # files subtree
          value.setBackground(BRUSH_TARGET)
          self.model.setItem(i, 2, value)
          value = QStandardItem(str(dir[3]))   #files tree
          value.setBackground(BRUSH_TARGET)
          self.model.setItem(i, 3, value) #
          value = QStandardItem(str(dir[4]))   #files all
          value.setBackground(BRUSH_TARGET)
          self.model.setItem(i, 4, value)
          value = QStandardItem(str(dir[5]))   #files all subtree
          value.setBackground(BRUSH_TARGET)
          self.model.setItem(i, 5, value)
          value = QStandardItem(str(dir[6]))   #files all tree
          value.setBackground(BRUSH_TARGET)
          self.model.setItem(i, 6, value)



          value = QStandardItem(str(dir[7]))   #size
          value.setBackground(BRUSH_SIZE)
          self.model.setItem(i, 7, value) #
          value = QStandardItem(str(dir[8]))   # size subtree
          value.setBackground(BRUSH_SIZE)
          self.model.setItem(i, 8, value)
          value = QStandardItem(str(dir[9]))   #size all
          value.setBackground(BRUSH_SIZE)
          self.model.setItem(i, 9, value)
          value = QStandardItem(str(dir[10]))   #size all subtree
          value.setBackground(BRUSH_SIZE)
          self.model.setItem(i, 10, value)
          value = QStandardItem(str(dir[11]))   #size all
          value.setBackground(BRUSH_SIZE)
          self.model.setItem(i, 11, value)
          value = QStandardItem(str(dir[12]))   #size all subtree
          value.setBackground(BRUSH_SIZE)
          self.model.setItem(i, 12, value)





        #[d, topselectedcnt, subtreeselectedcnt,  treeselectedcnt, topcnt, subtreecnt,  treecnt,  topselectedsize, subtreeselectedsize, treeselectedsize , topsize, subtreesize, treesize ]

        self.model.setHorizontalHeaderLabels( ['directory','# files','# files subtree','# files tree','# files all', '# files all subtree','# files all tree','# size','# size subtree','# size tree','# size all','#size all subtree', '# size all tree'            ])
        self.resizeColumnToContents(0)
        self.setSortingEnabled(True)



    def on_directory_clicked(self,item):

        # Achtung beide on_ callbacks werden im Konstruktor gesetzt, d.h. es werden immer beide
        # callbacks gerufen. Daher muss festgestellt werden, welches Proxymodell (Liste) genau dahintersteht ...
        if not isinstance(self.proxymodel, ProxyModelDir):
            return

        index_directory    = self.proxymodel.index(item.row(),0)



        directory      = self.proxymodel.data(index_directory)
        command=''
        if item.column() == 0: # click auf directory
           command = 'nemo '+'\''+directory+'\''
        #  Ordner anzeigen mit dem richtigen Tool ...
        if command: os.system(command)


    def on_file_clicked(self, item):
        # Achtung beide on_ callbacks werden im Konstruktor gesetzt, d.h. es werden immer beide
        # callbacks gerufen. Daher muss festgestellt werden, welches Proxymodell (Liste) genau dahintersteht ...
        if not isinstance(self.proxymodel, ProxyModelFiles):
            return


        index_suffix    = self.proxymodel.index(item.row(),0)
        index_file      = self.proxymodel.index(item.row(),1)
        index_name      = self.proxymodel.index(item.row(),2)
        index_directory = self.proxymodel.index(item.row(),3)

        suffix     = self.proxymodel.data(index_suffix)
        file       = self.proxymodel.data(index_file)
        name       = self.proxymodel.data(index_name)
        directory  = self.proxymodel.data(index_directory)


        command=''


        if item.column() == 1: # click auf file
          # falls auf ein xfpf stream geclickt wird, soll derselbige gerecorded werden ...
          ss=file
          if ss.endswith('xspf'):
            #command = 'streamripper http://91.250.77.9:8070 -u gaudi'
            command = 'gnome-terminal --command=\'streamripper ' + Util.get_url_stream(ss) + ' -d /home/user/astreamrip -u gaudi\''

          #command = 'xdg-open '+'\''+item.text()+'\''
          # das File muss in Hochkommata stehen, da der finename ein blank enthalten kann
        if item.column() == 2: # click auf filename
          command = 'xdg-open '+'\''+file+'\''
          # das Directory muss in Hochkommata stehen, da der finename ein blank enthalten kann
        if item.column() == 3: # click auf directory
          command = 'nemo '+'\''+file+'\''

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


        self.editA = QTextEdit()
        self.editA.textChanged.connect(self.on_text_changedA)
        text = self.daoConfig.value_get( CONFIG_SOURCEA , 'Please select a Directory' )
        self.editA.setText(text)

        butA = QPushButton('Source A')
        butA.clicked.connect(self.on_button_clickedA)
        layouttab3.addRow(butA, self.editA)







        self.editB = QTextEdit()
        self.editB.textChanged.connect(self.on_text_changedB)
        text = self.daoConfig.value_get(CONFIG_SOURCEB, 'Please select a Directory')
        self.editB.setText(text)

        butB = QPushButton('Source B')
        butB.clicked.connect(self.on_button_clickedB)
        layouttab3.addRow(butB,  self.editB)



        self.editC = QLineEdit()
        self.editC.textChanged.connect(self.on_text_changedC)
        text = self.daoConfig.value_get(CONFIG_TARGET, 'Please select a Directory')
        self.editC.setText(text)

        butC = QPushButton('Target')
        butC.clicked.connect(self.on_button_clickedC)
        layouttab3.addRow(butC,  self.editC)

        #self.checkLabel = QLabel('allow Delete')
        self.check = QCheckBox('allow Delete')
        chk = self.daoConfig.value_get(CONFIG_ALLOWDEL,' ')
        if chk == 'X':
          self.check.setChecked(True)
        else:
          self.check.setChecked(False)
        self.check.stateChanged.connect(self.on_delallowchanged)
        layouttab3.addRow( self.check )

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
        action_calculate      = QAction('Calculate', self)
        action_expand         = QAction('Expand', self)
        action_advanced       = QAction('Advanced', self)
        action_Indexing.triggered.connect(self.submitIndexing)
        action_DedupSpace.triggered.connect(self.submitDedupSapce)
        action_reduce.triggered.connect(self.submitReduce)
        action_calculate.triggered.connect(self.submitCalculate)
        action_advanced.triggered.connect(self.submitAdvanced)
        action_expand.triggered.connect(self.submitExpand)


        toolbar = QToolBar()
        toolbar.addAction(action_Indexing)
        toolbar.addAction(action_DedupSpace)
        toolbar.addAction(action_reduce)
        toolbar.addAction(action_calculate)
        toolbar.addAction(action_expand)
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
        newpath = QFileDialog(self,"Bitte Directory auswaehlen","/home/user").getExistingDirectory(self)
        if newpath:
          # neuen Pfad zu den bereits abgespeicherten Pfaden addieren ...
          text=self.editA.toPlainText()
          if text:
            text+='\n'   # nur falls text vorhanden war, soll dieser durch einen Zeilenumbruch vom neuen Pfad getrennt werden
          text+=newpath
          self.editA.setText(text)
          self.daoConfig.value_set(CONFIG_SOURCEA,text)



    def on_button_clickedB(self):
        newpath = QFileDialog(self,'Bitte Directory auswaehlen','/home/user').getExistingDirectory(self)
        if newpath:
          # neuen Pfad zu den bereits abgespeicherten Pfaden addieren ...
          text=self.editB.toPlainText()
          if text:
            text+='\n'   # nur falls text vorhanden war, soll dieser durch einen Zeilenumbruch vom neuen Pfad getrennt werden
          text+=newpath
          self.editB.setText(text)
          self.daoConfig.value_set(CONFIG_SOURCEB,text)

    def on_button_clickedC(self):
        newpath = QFileDialog(self,'Bitte Directory auswaehlen','/home/user').getExistingDirectory(self)

        self.editC.setText(newpath)
        self.daoConfig.value_set(CONFIG_TARGET,newpath)




    def on_text_changedA(self):
        # persistieren, sobald sich die Pfade im text geaendert haben ...
        text=self.editA.toPlainText()
        self.daoConfig.value_set(CONFIG_SOURCEA,text)

    def on_text_changedB(self):
        # persistieren, sobald  ch die Pfade im text geaendert haben ...
        text=self.editB.toPlainText()
        self.daoConfig.value_set(CONFIG_SOURCEB,text)
    def on_text_changedC(self):
        # persistieren, sobald sich die Pfade im text geaendert haben ...
        text=self.editC.text()
        self.daoConfig.value_set(CONFIG_TARGET,text)

    def on_delallowchanged(self):
        chk=self.check.checkState()
        if chk:
          self.daoConfig.value_set(CONFIG_ALLOWDEL,'X')
        else:
          self.daoConfig.value_set(CONFIG_ALLOWDEL,' ')


    def submitIndexing(self):
        print('Begin Indexing')
        Api.selection(daoA)
        Api.count_files(self.daoA)
        self.matrixA.display()

        Api.selection(daoB)
        Api.count_files(self.daoB)
        self.matrixB.display()
        print('End Indexing')

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

    def submitCalculate(self):
            print('Begin Calculate ')
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


            print('Ende Calculate ')

    def submitAdvanced(self):
            print('Begin Advanced ')

            print('Ende Advanced ')
        #if name == "":
            #QMessageBox.information( self, "Empty Field",
            #                        "Please enter a name and address.")


    def submitExpand(self):
            print('Begin Expand A ')
            Api.count_files(self.daoA,False)
            self.matrixA.display()
            print('End Expand A')
            print('Begin Expand B')
            Api.count_files(self.daoB,False)
            self.matrixB.display()
            print('End Expand B')








daoA = Dao(DATA_SOURCE_A)
daoB = Dao(DATA_SOURCE_B)
daoConfig = DaoConfig()



app = QApplication(sys.argv)
screen = Form( daoA, daoB, daoConfig )
screen.show()


sys.exit(app.exec_())











