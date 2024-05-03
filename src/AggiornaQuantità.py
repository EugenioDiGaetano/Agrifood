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
        # Recupero dell'ID del post, della quantità da aggiungere e della password dalla payload dell'evento
        post_id = event.get('post_id')
        password = event.get('password')
        quantity_to_add = event.get('qta_add')
        
        if not post_id or not quantity_to_add or not password:
            # Controllo di validità dei dati forniti
            return {
                'statusCode': 400,
                'body': json.dumps('ID del post, quantita\' da aggiungere o password mancante.')
            }
            
        # Recupera il nome della tabella DynamoDB dal parametro di AWS Systems Manager Parameter Store
        table_name = ssm_client.get_parameter(Name=parameter_name)['Parameter']['Value']
        
        # Ottiene la tabella DynamoDB
        table = dynamodb.Table(table_name)
        
        # Recupero dell'item corrente dal database
        response = table.get_item(Key={'Id': post_id})
        item = response.get('Item')
        
        if not item:
            # Restituzione di un errore se l'item non esiste
            return {
                'statusCode': 400,
                'body': json.dumps('Post non trovato.')
            }
            
        if response['Item'].get('password') != password:
            # Restituzione di un errore se la password è errata
            return {
                'statusCode': 401,
                'body': json.dumps('Password errata')
            }
        
        # Recupero della quantità corrente disponibile e della quantità massima
        current_quantity = item.get('quantity', 0)
        max_qta = item.get('totalQuantity')
        
        # Calcolo della nuova quantità dopo l'aggiunta
        new_quantity = current_quantity + quantity_to_add
        
        # Verifica se la nuova quantità supera la quantità massima consentita
        if new_quantity > max_qta:
            return {
                'statusCode': 400,
                'body': json.dumps('Quantita\' massima superata.')
            }
        
        # Verifica se la quantità da aggiungere è negativa
        if quantity_to_add < 0:
            return {
                'statusCode': 400,
                'body': json.dumps('La quantita\' da aggiungere non può essere negativa.')
            }
        
        # Verifica se la quantità da aggiungere è zero
        if quantity_to_add == 0:
            return {
                'statusCode': 400,
                'body': json.dumps('La quantita\' da aggiungere non può essere zero.')
            }
        
        # Aggiornamento dell'item nel database con la nuova quantità
        table.update_item(
            Key={'Id': post_id},
            UpdateExpression='SET quantity = :val',
            ExpressionAttributeValues={':val': new_quantity}
        )
        
        # Restituzione di una risposta di successo
        return {
            'statusCode': 200,
            'body': json.dumps('Quantita\' disponibile aggiornata con successo.')
        }
    except Exception as e:
        # Restituzione di un errore generico se si verifica un'eccezione
        return {
            'statusCode': 500,
            'body': json.dumps('Errore durante l\'aggiornamento della quantita\' disponibile')
        }
