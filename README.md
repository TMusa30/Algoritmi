Korištenje programa !

Program solution.py koristi se za pronalaženje najkraćeg puta između čvorova u grafu. Možeš koristiti jedan od sljedećih algoritama: BFS, UCS ili A*


Parametri :
  1. --alg <algoritam>: Određuje koji algoritam će se koristiti. Moguće vrijednosti su bfs, ucs, i astar.
  2. --ss <datoteka>: Putanja do datoteke koja sadrži informacije o grafu.
  3. --h <heuristika>: Putanja do datoteke koja sadrži heuristike.

Pokretanje programa !
Program se pokreće iz command prompt-a ili terminala koristeći Python i zahtijeva određene parametre. Evo primjera kako pokrenuti program :

1. BFS algoritam :
   "python solution.py --alg bfs --ss istra.txt" -> koristi se istra.txt datoteka za pronalaženje najkraćeg puta !

2. UCS algoritam :
   "python solution.py --alg ucs --ss test_case_1.txt"
   
3. "python solution.py --alg astar --ss istra.txt --h istra_heuristic.txt"

   

