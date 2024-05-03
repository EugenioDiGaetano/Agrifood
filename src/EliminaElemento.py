import json
import boto3

# Crea un client per AWS Systems Manager Parameter Store
ssm_client = boto3.client('ssm')

# Creazione di una risorsa DynamoDB
dynamodb = boto3.resource('dynamodb')

# Nome del parametro che contiene il nome della tabella
parameter_name = '/TableName'

def lambda_handler(event, context):
    try:
        # Recupera il nome della tabella DynamoDB dal parametro di AWS Systems Manager Parameter Store
        table_name = ssm_client.get_parameter(Name=parameter_name)['Parameter']['Value']
        
        # Ottiene la tabella DynamoDB
        table = dynamodb.Table(table_name)
        
        # Recupero dell'ID del post e della password dalla payload dell'evento
        post_id = event.get('post_id')
        password = event.get('password')
        
        if not post_id or not password:
            # Controllo di validità dei dati forniti
            return {
                'statusCode': 400,
                'body': json.dumps('ID del post o password mancante.')
            }
        
        # Recupero dell'item dal database
        response = table.get_item(Key={'Id': post_id})
        
        if 'Item' not in response:
            # Restituzione di un errore se l'item non esiste
            return {
                'statusCode': 400,
                'body': json.dumps('Post non trovato.')
            }
        
        # Verifica se la password corrisponde
        if response['Item'].get('password') != password:
            # Restituzione di un errore se la password è errata
            return {
                'statusCode': 401,
                'body': json.dumps('Password errata')
            }
        
        # Eliminazione dell'item dal database
        table.delete_item(Key={'Id': post_id})
        
        # Restituzione di una risposta di successo
        return {
            'statusCode': 200,
            'body': json.dumps('Il post e\' stato eliminato con successo.')
        }
    except Exception as e:
        # Restituzione di un errore generico se si verifica un'eccezione
        return {
            'statusCode': 500,
            'body': json.dumps('Errore durante l\'eliminazione del post')
        }
