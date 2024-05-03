import json
import boto3
from time import strftime
import uuid

# Crea un client per AWS Systems Manager Parameter Store
ssm_client = boto3.client('ssm')

# Creazione di una risorsa DynamoDB
dynamodb = boto3.resource('dynamodb')

# Nome del parametro che contiene il nome della tabella
parameter_name = '/TableName'
    
def lambda_handler(event, context):
    # Ottenimento dell'orario corrente
    now = strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Recupera il nome della tabella DynamoDB dal parametro di AWS Systems Manager Parameter Store
        table_name = ssm_client.get_parameter(Name=parameter_name)['Parameter']['Value']
        
        # Ottiene la tabella DynamoDB
        table = dynamodb.Table(table_name)
        
        # Generazione di un nuovo UUID come chiave primaria per ogni chiamata della funzione
        post_id = str(uuid.uuid4())
        
        # Costruzione dell'oggetto post_item con i dati forniti nell'evento
        post_item = {key: value for key, value in event.items()}
        
        # Aggiunta della data di inserimento e della chiave primaria
        post_item['date'] = now
        post_item['Id'] = post_id
        
        # Inserimento dell'elemento nella tabella DynamoDB
        table.put_item(Item=post_item)
        
        # Restituisce una risposta di successo
        return {
            'statusCode': 200,
            'body': json.dumps('Il tuo post e\' stato aggiunto con successo')
        }
    except Exception as e:
        # Gestione delle eccezioni e restituzione di un messaggio di errore dettagliato
        return {
            'statusCode': 500,
            'body': json.dumps('Si e\' verificato un errore durante l\'inserimento del post')
        }