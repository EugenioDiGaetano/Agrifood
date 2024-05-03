# Agrifood
Agrifood è una piattaforma web concepita per agevolare il processo di compravendita di prodotti agricoli a chilometro zero tramite una bacheca online, incentrata sulle transazioni dirette tra privati. L'obiettivo primario di Agrifood è quello di fornire agli utenti un ambiente digitale intuitivo e affidabile, finalizzato alla pubblicazione e alla ricerca di prodotti agricoli freschi e di eccellente qualità.

## Funzionalità principali:
- **Pubblicazione dei Prodotti:** Gli utenti possono pubblicare i loro prodotti agricoli sulla bacheca online, fornendo informazioni dettagliate come descrizione del prodotto, tecniche di coltivazione e quantità disponibile.
- **Ricerca dei Prodotti:** Gli utenti possono cercare prodotti agricoli utilizzando vari criteri come tipo di prodotto, metodo di coltivazione, ecc.
- **Gestione delle Prenotazioni di Acquisto:** Gli utenti possono effettuare prenotazioni di acquisto non vincolanti per i prodotti che desiderano acquistare. Il sistema gestisce automaticamente le prenotazioni e aggiorna la quantità disponibile.
- **Eliminazione Automatica dei Prodotti Scaduti:** Una funzione automatica elimina i prodotti scaduti dalla bacheca dopo un determinato periodo di tempo, garantendo che solo prodotti freschi siano disponibili per l'acquisto.

## Architettura del Sistema
Il sistema Agrifood si basa su un'architettura serverless utilizzando i servizi AWS Lambda, API Gateway, DynamoDB, AWS Amplify, Systems Manager e Amazon EventBridge. Le richieste degli utenti vengono gestite tramite API Gateway e Lambda, mentre DynamoDB funge da database per memorizzare i dati dei prodotti e le prenotazioni di acquisto. AWS Amplify viene utilizzato per lo sviluppo dell'interfaccia web frontend, semplificando la gestione dell'infrastruttura di backend. Systems Manager consente la gestione centralizzata dei parametri di configurazione, mentre Amazon EventBridge gestisce i trigger sul database DynamoDB per mantenere pulita la base di dati.

![Impossibile caricare l'immagine](https://github.com/EugenioDiGaetano/Agrifood/blob/main/report/architettura.jpg?raw=true)

## Istruzioni per l'esecuzione del codice
1. Creare un parametro di tipo stringa su AWS Systems Manager che si chiami 'TableName' che corrisponde al nome della tabella su Dynamodb.
2. Creare le funzioni lambda importando i file presenti nella cartella `/src` su Aws Lambda.
3. Creare un nuovo Gateway Rest API importando il file `/api.json` ed adattandolo alle funzioni precedentemente create.
4. Creare un nuovo stage(fase) per il Gateway creato.
5. Inserire i link nel file `/static/url.json`.
6. Creare due pianificazioni per le funzioni di pulizia e ripristino.
7. Comprimere il contenuto della catrtella static in un file zip e caricarlo su AWS Amplify.

## API

Una descrizione dettagliata delle funzioni è disponibile nella cartella `/report` all'interno di questo repository. Il file contiene informazioni sulle funzionalità, sui dati richiesti in ingresso e sull'output.

## Report

Il report completo del progetto è disponibile nella cartella `/report` all'interno di questo repository. Il report segue la struttura di un articolo scientifico e include dettagli sul design della soluzione e le conclusioni.
