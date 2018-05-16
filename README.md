# README.md

Elenco di script:

- report_period_pbs.py
- report_userPeriod_pbs.py
- report_status_pbs_py
- report_walltime_pbs.py

## REPORT_PERIOD_PBS.PY
Lo script prende due parametri in input: 
	param1: nome del file di inizio periodo
	param2: nome del file di fine periodo
Esempio di lancio script:

```python ./report_period_pbs.py 20180101 20180331```

Lo script crea una cartella LOGS_Period all'interno della home directory dell'utente (directory da cui viene lanciato lo script).
All'interno della cartella viene creto un file con il nome "log_periodoinizio_periodofine.txt" che riporta il resoconto di tutti i job eseguiti da tutti gli utenti che hanno eseguito job in quel periodo.
Il file sopra citato riporta:
- l'intervallo temporale di considerazione
- ogni utente con a seguire il numero di job per il primo file del periodo, riportando lo stato di uscita del job, il walltime e la cputime utilizzata da ogni job. Alla fine di ogni file viene riportato un sommario di tutti i job eseguiti dall'utente per ogni file e il walltime e cputime totale per file. 

Le informazioni riportate nell'ultimo punto vengono mostrate per ogni utente presente nell'intervallo di tempo considerato.


## REPORT_USERPERIOD_PBS.PY
Per essere eseguito lo script prende in input tre parametri:
 1 - nome utente nel formato nome.cognome
 3 - file di log da cui iniziare a registrare la cputime e il walltime
 4 - file di log da cui fermarsi nel registrare la cputime e il walltime

Esempio di lancio script:

```python ./reporst_userPeriod_pbs.py alessia.tovo 20180101 20180331```

Lo script crea una cartella LOGS_UserPeriod all'interno della home directory dell'utente (directory da cui viene lanciato lo script).
All'interno della cartella viene creato un file con il nome "log_periodoinizio_periodofine.txt" che riporta il resoconto di tutti i job eseguiti dall'utente nome.cognome nel periodo indicato.
Il file sopra citato riporta:
 - l'intervallo temporale di considerazione 
 - la lista, per ogni file, dei job contenuti in esso e, se presente, il walltime e cputime per ogni job, e al termine del file, il totale cputime e walltime utilizzato in quel file
 - un resoconto finale che indica il totale numero di job nel periodo indicato, la cputime totale per il periodo indicato, la walltime totale per il periodo indicato


## REPORT_STATUS_PBS.PY
Lo script prende due parametri in input: 
	param1: nome del file di inizio periodo
	param2: nome del file di fine periodo
Esempio di lancio script:

```python ./report_status_pbs.py 20180101 20180331```

Lo script crea una cartella LOGS_StatusPeriod all'interno della home directory dell'utente (directory da cui viene lanciato lo script).
All'interno della cartella viene creato un file con il nome "log_periodoinizio_periodofine.txt" che riporta il resoconto di tutti i job eseguiti dall'utente nome.cognome nel periodo indicato.
Il file sopra citato riporta:
- l'intervallo temporale di considerazione
- il nome di ogni utente trovato, il numero di jobs per ogni file e la lista di jobs. Il numero e l'elenco di jobs con status = Ok, il numero e l'elenco di jobs con status = error, il numero e l'elenco di jobs con status = Killed manually, il numero e l'elenco di jobs con status non identificato.

## REPORT_WALLTIME_PBS.PY
Lo script prende tre parametri in input: 
	param1: nome del file di inizio periodo
	param2: nome del file di fine periodo
	param3: walltime nel formato hh:mm_ss
Esempio di lancio script:

```python ./report_walltime_pbs.py 20180101 20180331```

Lo script crea una cartella LOGS_StatusPeriod all'interno della home directory dell'utente (directory da cui viene lanciato lo script).
All'interno della cartella viene creato un file con il nome "log_periodoinizio_periodofine.txt" che riporta il resoconto di tutti i job eseguiti dall'utente nome.cognome nel periodo indicato.
Il file sopra citato riporta:
- l'intervallo temporale di considerazione
- l'elenco di job, con il rispettivo walltime, che supera , o è uguale, al walltime in input
- al termine, l'elenco completo di tutti i job nel periodo considerato, che superano o sono uguali al walltime preso in input




