## Funzione 1: HomePage (Recupera tutti gli elementi dalla tabella)

**Input:**
- `event:` L'evento inviato alla funzione Lambda. Non richiede input specifici.
- `context:` Il contesto dell'esecuzione della funzione Lambda.

**Output:**
- `statusCode:` Lo stato della richiesta HTTP. Può essere 200 per successo o 500 per errore.
- `body:` Un oggetto JSON che contiene tutti gli elementi della tabella.

**Descrizione:**
Questa funzione recupera tutti gli elementi dalla tabella DynamoDB, escludendo il campo "password" per motivi di sicurezza. Restituisce una lista di tutti gli elementi recuperati.

---

## Funzione 2: AggiungiElemento (Aggiunge un nuovo post)

**Input:**
- `event:` L'evento inviato alla funzione Lambda che contiene i dati del nuovo post da aggiungere.
- `context:` Il contesto dell'esecuzione della funzione Lambda.

**Output:**
- `statusCode:` Lo stato della richiesta HTTP. Può essere 200 per successo o 500 per errore.
- `body:` Un oggetto JSON che contiene un messaggio di successo o errore.

**Descrizione:**
Questa funzione aggiunge un nuovo post alla tabella DynamoDB. Genera un ID univoco per il post, aggiunge la data corrente e inserisce l'elemento nella tabella.

---

## Funzione 3: EliminaElemento (Elimina un post)

**Input:**
- `event:` L'evento inviato alla funzione Lambda che contiene l'ID del post da eliminare e la relativa password.
- `context:` Il contesto dell'esecuzione della funzione Lambda.

**Output:**
- `statusCode:` Lo stato della richiesta HTTP. Può essere 200 per successo, 400 per errore nei dati forniti o 500 per errore interno.
- `body:` Un oggetto JSON che contiene un messaggio di successo o errore.

**Descrizione:**
Questa funzione elimina un post dalla tabella DynamoDB. Verifica prima se l'ID del post e la password forniti sono corretti, quindi elimina l'elemento dalla tabella.

---

## Funzione 4: Prenota (Sottrae la quantità richiesta dal post)

**Input:**
- `event:` L'evento inviato alla funzione Lambda che contiene l'ID del post e la quantità da sottrarre.
- `context:` Il contesto dell'esecuzione della funzione Lambda.

**Output:**
- `statusCode:` Lo stato della richiesta HTTP. Può essere 200 per successo, 400 per errori nei dati forniti o 500 per errore interno.
- `body:` Un oggetto JSON che contiene un messaggio di successo o errore.

**Descrizione:**
Questa funzione sottrae la quantità richiesta da un post nella tabella DynamoDB. Verifica se l'ID del post e la quantità da sottrarre sono validi, quindi aggiorna la quantità disponibile del post. Se la quantità richiesta è maggiore della quantità disponibile, viene restituito un errore.

---

## Funzione 5: AggiornaQuantità (Aggiorna la quantità disponibile)

**Input:**
- `event:` L'evento inviato alla funzione Lambda che contiene l'ID del post, la password e la quantità da aggiungere.
- `context:` Il contesto dell'esecuzione della funzione Lambda.

**Output:**
- `statusCode:` Lo stato della richiesta HTTP. Può essere 200 per successo, 400 per errori nei dati forniti o 500 per errore interno.
- `body:` Un oggetto JSON che contiene un messaggio di successo o errore.

**Descrizione:**
Questa funzione aggiorna la quantità disponibile di un post nella tabella DynamoDB. Verifica se l'ID del post e la password forniti sono corretti e se la quantità da aggiungere è valida, quindi aggiorna la quantità disponibile del post.

---

## Funzione 6: EliminaVecchiElementi (Elimina post meno recenti)

**Input:**
- `event:` L'evento inviato alla funzione Lambda. Non richiede input specifici.
- `context:` Il contesto dell'esecuzione della funzione Lambda.

**Output:**
- `statusCode:` Lo stato della richiesta HTTP. Può essere 200 per successo o 500 per errore.
- `body:` Un oggetto JSON che contiene un messaggio di successo o errore.

**Descrizione:**
Questa funzione elimina i post meno recenti dalla tabella DynamoDB. Utilizza un parametro di AWS Systems Manager Parameter Store per ottenere il nome della tabella e poi esegue una scansione della tabella per trovare i post inseriti più di una settimana fa. Gli elementi trovati vengono eliminati dalla tabella.

---

## Funzione 7: RipristinaQuantità (Aggiorna la quantità disponibile per post esauriti)

**Input:**
- `event:` L'evento inviato alla funzione Lambda. Non richiede input specifici.
- `context:` Il contesto dell'esecuzione della funzione Lambda.

**Output:**
- `statusCode:` Lo stato della richiesta HTTP. Può essere 200 per successo o 500 per errore.
- `body:` Un oggetto JSON che contiene un messaggio di successo o errore.

**Descrizione:**
Questa funzione aggiorna la quantità disponibile di tutti i post esauriti (con quantità pari a zero) nella tabella DynamoDB. Recupera gli elementi con quantità zero, quindi imposta la quantità disponibile al valore dell'ultima quantità prenotata.