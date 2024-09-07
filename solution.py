import sys
from collections import deque
import heapq


class myDictionary(dict):
    def add(self, key, value):
        if key not in self:
            self[key] = []
        self[key].append(value)

#sortiranje liste koristio kod provjere konzistentnosti jer je bitan redoslijed ispisa
def sortiraj(lista) :
   heapq.heapify(lista)
   sortiranaLista = []
   while lista :
      sortiranaLista.append(heapq.heappop(lista))
   return sortiranaLista

#metoda kojoj ako damo kao listu neku putanju primjer ["Pula", "Barban", "Labin"] i jos damo prijelaze izmedu njih
#i zavrsno stanje ona ce izracunat i vratit cijenu prijelaza izmedu ["Pula", "Barban", "Labin"]
#Koristio sam ju za sve algoritme
def izracunajCijenu(putanja, prijelazi, zavrsnoStanje):
    totalCost = 0.0
    
    if len(putanja) == 1 :
      #Slucaj kad se posalje susjed od zavrsnoStanja kod astar algoritma sam koristio
      for prijelaz in prijelazi :
         pocetnaDestinacija, destinacije = prijelaz.split(":")
         destinacije = destinacije.split()
         
         if pocetnaDestinacija == putanja[0]:
            for destinacija in destinacije :
               splitajDestinacija = destinacija.split(",")
               
               if splitajDestinacija[0] == zavrsnoStanje[0]:
                  return splitajDestinacija[1]
    else :
      for i in range(len(putanja) - 1):
        
        for prijelaz in prijelazi:
            pocetnaDestinacija, destinacije = prijelaz.split(":")
            destinacije = destinacije.split()
            if putanja[i] == pocetnaDestinacija :
              for destinacija in destinacije:
                 kojiJeSusjed = destinacija.split(",")
                 susjedGrad = kojiJeSusjed[0]
                 susjedPrijelazCijena = float(kojiJeSusjed[1])
                 if susjedGrad == putanja[i+1]:
                    totalCost += susjedPrijelazCijena
                    break        
                
    return totalCost

#metoda kojoj ako posaljem graf vratit ce mi sve moguce puteve od pocetnoStanja do zavrsnog stanja
def sviPutevi(graf, pocetnoStanje, zavrsnaStanja):
    
      red = deque([(pocetnoStanje, [pocetnoStanje])])
      sviCestovniPutevi = []

      while red :
          treutnoStanje, putanjaStanje = red.popleft()
          #ovdje sam dodao jos ovaj or (len(zavrsnaStanja) > 1) and trenutnoStanje == zavrsnaStanja[1] da
          #provjerava kad ima i vise zavrsnih stanja
          if treutnoStanje == zavrsnaStanja[0] or (len(zavrsnaStanja) > 1 and treutnoStanje == zavrsnaStanja[1]):
            
              sviCestovniPutevi.append(putanjaStanje)
          else :
            for susjed in graf[treutnoStanje]:
                if susjed not in putanjaStanje:
                    red.append((susjed, putanjaStanje + [susjed]))

      return sviCestovniPutevi

#Ova metoda kad joj damo neki grad tj. cvor i datoteku u kojoj su zapisane heuristike racuna heuristiku
#tog mjesta -> koristio sam kod konzistenstnosti
def izracunajHeuristikuDrugog(mjesto,datotekaIterirat) :
    
    for linija in datotekaIterirat : 
        heuristickiGradZaUsporedit, cijenaHeuristikeOdMetode = linija.split(":")
        
        if heuristickiGradZaUsporedit == mjesto:
            return float(cijenaHeuristikeOdMetode)
    return 0
def bfs(pocetnoStanje, zavrsnaStanja, prijelazi) :
  putanja = myDictionary()

   #prijelaze zelim sve splitat po opcijama kojim mogu i onda napravit za neku lokaciju da to bude kljuc a njegove vrijednosti susjedi (jos nije sigurno jel bi to radilo)
  for prijelaz in prijelazi :
    
    splitajPrijelazePoDvotocci = prijelaz.split(":")
    pocetnaDestinacija = splitajPrijelazePoDvotocci[0]
    pocetnaDestinacijaSusjedi = splitajPrijelazePoDvotocci[1]

    #sljedeci korak sam uzeo s interneta za splitanje po razmaku nisam znao kako tocno ide sintaksa : https://www.w3schools.com/python/ref_string_split.asp

    susjediSplitaniPoRazmaku = pocetnaDestinacijaSusjedi.split()
    
    putanja[pocetnaDestinacija] = []
    if susjediSplitaniPoRazmaku :
      for susjedOdPocetne in susjediSplitaniPoRazmaku :
        x = susjedOdPocetne.split(",")
        imeSusjedskogNaselja = x[0]
        cijenaPrijelazaUSusjedskiGrad = x[1]
        putanja.add(pocetnaDestinacija, imeSusjedskogNaselja) #izgradanja dictionarya di je kljuc odreden grad a vrijednosti su njegovi susjedi

  beskonacnost = (10**8) #definirana beskonacnost da spremimo prvi put kad prolazi petlja
  returnajPravuPutanju = None
  for zavrsnoStanje in zavrsnaStanja:
    visited = set()
    red = deque([pocetnoStanje])
    putanjaBFS = deque([[pocetnoStanje]])

    while red:
      
      node = red.popleft()
      putanjaDoCilja = putanjaBFS.popleft()
      
      if node not in visited :
          visited.add(node)
          if node == zavrsnoStanje :
            if len(visited) < beskonacnost:
             beskonacnost = len(visited)
             returnajPravuPutanju = putanjaDoCilja
      for susjed in putanja[node] :
         if susjed not in visited :
            red.append(susjed)
            putanjaBFS.append(putanjaDoCilja + [susjed])
  if returnajPravuPutanju :
     return returnajPravuPutanju, len(visited)
  else :
     return [], 0

def ucs(pocetnoStanje, zavrsnaStanja, prijelazi) :
  putanja = myDictionary()
  for prijelaz in prijelazi :
    
    splitajPrijelazePoDvotocci = prijelaz.split(":")
    pocetnaDestinacija = splitajPrijelazePoDvotocci[0]
    pocetnaDestinacijaSusjedi = splitajPrijelazePoDvotocci[1]

    susjediSplitaniPoRazmaku = pocetnaDestinacijaSusjedi.split()
    
    putanja[pocetnaDestinacija] = []
    if susjediSplitaniPoRazmaku :
      for susjedOdPocetne in susjediSplitaniPoRazmaku :
      
        putanja.add(pocetnaDestinacija, susjedOdPocetne) #izgradnja dictionarya gdje je kljuc neki grad, a vrijednosti su njegovi susjedi (s cijenom prijelaza)

  

  visited = set()
  red = []
  red.append((0.0, [pocetnoStanje]))
  visitedStates = 0
  
  while red :
      
      var = heapq.heappop(red)
      cijena = var[0]
      putanjaTrazena = var[1]
     
      node = putanjaTrazena[-1]
     
      if node == zavrsnoStanje[0] or (len(zavrsnaStanja) > 1 and node == zavrsnoStanje[1]):
        
          putanjaUCS = putanjaTrazena
          break
      
      if node not in visited :
          visited.add(node)
          visitedStates += 1
          for susjed in putanja[node] :
            if susjed not in visited:
              rastaviSusjedaPoZarezu = susjed.split(",")
              susjedRastavljenPoZarezu = rastaviSusjedaPoZarezu[0]
              cijenaPrijelazaRastavljenoPoZarezu = float(rastaviSusjedaPoZarezu[1])
              novaPutanja = putanjaTrazena + [susjedRastavljenPoZarezu]
              novaCijena = cijena + cijenaPrijelazaRastavljenoPoZarezu
              heapq.heappush(red, (novaCijena, novaPutanja))
  if putanjaUCS :
     return putanjaUCS, izracunajCijenu(putanjaUCS, prijelazi, zavrsnaStanja),visitedStates
  else :
     return None

def astar(pocetnoStanje, zavrsnaStanja, prijelazi, ulazDatotekeHeuristike) :
    putanja = myDictionary()
    for prijelaz in prijelazi :
    
      splitajPrijelazePoDvotocci = prijelaz.split(":")
      pocetnaDestinacija = splitajPrijelazePoDvotocci[0]
      pocetnaDestinacijaSusjedi = splitajPrijelazePoDvotocci[1]

    

      susjediSplitaniPoRazmaku = pocetnaDestinacijaSusjedi.split()
    
      putanja[pocetnaDestinacija] = []
      if susjediSplitaniPoRazmaku :
        for susjedOdPocetne in susjediSplitaniPoRazmaku :
      
          x = susjedOdPocetne.split(",")
          imeSusjedskogNaselja = x[0]
          cijenaPrijelazaUSusjedskiGrad = x[1]
          putanja.add(pocetnaDestinacija, imeSusjedskogNaselja)
    sviMoguciPutevi = sviPutevi(putanja, pocetnoStanje, zavrsnaStanja)
    #sviMoguciPutevi =[["Pula", "Vodnjan", "Kanfanar", "Žminj", "Pazin", "Motovun", "Buzet"]]
    
    beskonacnost = (10**8)
    statesVisited = 0
    for put in sviMoguciPutevi :
        
        spremiPredzadnji = [put[-2]]
       
        
        cijenaPuta = izracunajCijenu(put, prijelazi, zavrsnaStanja)
        
        
        
        
        statesVisited += 1
        for ulaz in ulazDatotekeHeuristike :
           splitanHeuristikaPoDvotocki = ulaz.split(":")
           gradHeuristike = splitanHeuristikaPoDvotocki[0]
           
           cijenaHeurisike = splitanHeuristikaPoDvotocki[1].strip()
           

           if put[-2] == gradHeuristike : #put[-2] predzadnji element u listi
              
              
              cijenaPuta += float(cijenaHeurisike)
           
        if cijenaPuta < beskonacnost :
          beskonacnost = cijenaPuta
          najboljaCijena = izracunajCijenu(put,prijelazi,zavrsnaStanja)
          najboljiPut = put
    return najboljiPut, najboljaCijena, statesVisited
  


  

argumenti = sys.argv

if "--ss" in argumenti :
  sacuvajIndexPrefiksaDatoteke = argumenti.index("--ss")
  uhvatiDatoteku = argumenti[sacuvajIndexPrefiksaDatoteke + 1]
  
  file = open(uhvatiDatoteku, "r", encoding="utf-8") #uzeo s ovog linka (citanje txt file-a) https://hackernoon.com/how-to-read-text-file-in-python
  sadrzajFile = file.read()

  #prvo se rijesit komentara u dokumentu
  
  splitajUlaz = sadrzajFile.strip().split("\n")
  komentari = []

  for line in splitajUlaz :     #pitati je li treba samo prvi znak linije ispitat je li komentar (ustvari nece se pojavit komentar negdje odjednom u liniji na recimo 10-om mjestu)
    if line[0] == "#":  
      komentari.append(line)
  for line in komentari :
    splitajUlaz.remove(line)

  pocetnoStanje = splitajUlaz[0]
  zavrsnoStanje = splitajUlaz[1].split()
  prijelazi = splitajUlaz[2:]

if "--h" in argumenti:
  sacuvajIndexPrefiksaDrugeDatoteke = argumenti.index("--h")
  uhvatiDruguDatoteku = argumenti[sacuvajIndexPrefiksaDrugeDatoteke + 1]

  file = open(uhvatiDruguDatoteku, "r", encoding="utf-8")

  sadrzajeFileDruge = file.read()

  splitajUlazDruge = sadrzajeFileDruge.strip().split("\n")
  komentari2 = []
  
  for line in splitajUlazDruge:
    if line[0] == "#":
      komentari2.append(line)
  for line in komentari2:
    splitajUlazDruge.remove(line)
  brojacOptimiscneHeuristike = 0
  if argumenti.__contains__("--check-optimistic"):
        print("# HEURISTIC-OPTIMISTIC " + uhvatiDruguDatoteku)

        for prijelaz in splitajUlazDruge :
          heuristickiGrad, heuristikaPrijelazVrijednost = prijelaz.split(":")
          heuristikaPrijelazVrijednost = heuristikaPrijelazVrijednost.strip()
          
          putOdHeuristickogDoCilja,cijenaHeuristickogPuta, statesVisited = ucs(heuristickiGrad, zavrsnoStanje, splitajUlaz[2:])
          
          if float(heuristikaPrijelazVrijednost) > cijenaHeuristickogPuta:
            stanje = "[ERR]"
            brojacOptimiscneHeuristike = 1
          else :
            stanje = "[OK]"
          print("[CONDITION]: " + stanje + " h(" + heuristickiGrad + ") <= h*: " + str(float(heuristikaPrijelazVrijednost)) + " <= " + str(float(cijenaHeuristickogPuta)))
        if brojacOptimiscneHeuristike == 0 :
            print("[CONCLUSION]: Heuristic is optimistic.")
        else :
            print("[CONCLUSION]: Heuristic is not optimistic.")
  elif(argumenti.__contains__("--check-consistent")):
     print("# HEURISTIC-CONSISTENT " + uhvatiDruguDatoteku)
     for prijelaz in splitajUlazDruge :
        splitanHeuristickiGrad, cijenaHeuristikeGrada = prijelaz.split(":")
        cijenaHeuristikeGrada = cijenaHeuristikeGrada.strip()
        for prijelaz in prijelazi :
           usporedniGrad, ostaliPrijelazi = prijelaz.split(":")
           uzmiSusjede = ostaliPrijelazi.split()
           sortiraniUzmiSusjede = sortiraj(uzmiSusjede)
           
           if splitanHeuristickiGrad == usporedniGrad :
              
              for uzmiSusjeda in sortiraniUzmiSusjede :
                 mjesto, cijenaSusjeda = uzmiSusjeda.split(",")
                 cijenaHeuristikeMjesto = izracunajHeuristikuDrugog(mjesto, splitajUlazDruge)
                 if float(cijenaHeuristikeGrada) > (cijenaHeuristikeMjesto + float(cijenaSusjeda)) :
                    stanje = "[ERR]"
                    brojacOptimiscneHeuristike += 1
                 else :
                    stanje = "[OK]"
                 print("[CONDITION]: " + stanje + " h(" + splitanHeuristickiGrad + ") <= h(" + mjesto + ") + c: " + str(float(cijenaHeuristikeGrada)) + " <= " + str(cijenaHeuristikeMjesto) + " + " + str(float(cijenaSusjeda)))
     if brojacOptimiscneHeuristike != 0 :
        print("[CONCLUSION]: Heuristic is not consistent.")
     else :
        print("[CONCLUSION]: Heuristic is consistent.")
              


for argument in argumenti :

  if argument == "--alg" :
    sacuvajIndexAlgoritma = argumenti.index("--alg")
    
    sacuvaj = argumenti[sacuvajIndexAlgoritma + 1]

    if sacuvaj == "bfs":
      sejvanaPutanjaBFS, posjecenaMjestaBFS = bfs(pocetnoStanje, zavrsnoStanje, prijelazi)
      if sejvanaPutanjaBFS :
           print("# BFS")
           print("[FOUND_SOLUTION]: yes")
           print("[STATES_VISITED]: " + str(posjecenaMjestaBFS))
           print("[PATH_LENGTH]: " + str(len(sejvanaPutanjaBFS)))
           print("[TOTAL_COST]: " + str(izracunajCijenu(sejvanaPutanjaBFS, prijelazi, zavrsnoStanje)))
           print("[PATH]: " + " => ".join(sejvanaPutanjaBFS))
      else :
           print("[FOUND_SOLUTION]: no")
    elif sacuvaj == "ucs":
      sejvanaPutanjaUCS,cijenaUCS, posjecenaMjestaUCS = ucs(pocetnoStanje, zavrsnoStanje, prijelazi)

      if sejvanaPutanjaUCS :
          print("# UCS")
          print("[FOUND_SOLUTION]: yes")
          print("[STATES_VISITED]: " + str(posjecenaMjestaUCS))
          print("[PATH_LENGTH]: " + str(len(sejvanaPutanjaUCS)))
          print("[TOTAL_COST]: " + str(cijenaUCS))
          print("[PATH]: " + " => ".join(sejvanaPutanjaUCS))
      else :
           print("[FOUND_SOLUTION]: no")
    else :
        putanjaASTAR, cijenaASTAR, posjecenaMjestaASTAR = astar(pocetnoStanje, zavrsnoStanje, prijelazi, splitajUlazDruge)
        if putanjaASTAR:
           print("# A-STAR " + uhvatiDruguDatoteku)
           print("[FOUND_SOLUTION]: yes")
           print("[STATES_VISITED]: " + str(posjecenaMjestaASTAR))
           print("[PATH_LENGTH]: " + str(len(putanjaASTAR)))
           print("[TOTAL_COST]: " + str(cijenaASTAR))
           print("[PATH]: " + " => ".join(putanjaASTAR))
        else :
           print("[FOUND_SOLUTION]: no")
