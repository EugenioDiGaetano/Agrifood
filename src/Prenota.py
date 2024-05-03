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
        # Recupero dell'ID del post e della quantità da sottrarre dalla payload dell'evento
        post_id = event.get('post_id')
        quantity_to_subtract = event.get('qta_subtract')
        
        if not post_id or not quantity_to_subtract:
            # Controllo di validità dei dati forniti
            return {
                'statusCode': 400,
                'body': json.dumps('ID del post o quantita\' da sottrarre mancante.')
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
        
        # Recupero della quantità corrente disponibile
        current_quantity = item.get('quantity', 0)
        max_qta = item.get('totalQuantity')

        # Controllo se la quantità richiesta è maggiore della quantità disponibile
        if current_quantity == 0:
            return {
                'statusCode': 400,
                'body': json.dumps('Il prodotto e\' terminato, si prega di riprovare piu\' tardi.')
            }
            
        # Controllo se la quantità richiesta è maggiore della quantità disponibile
        if quantity_to_subtract > current_quantity:
            return {
                'statusCode': 400,
                'body': json.dumps('Quantita\' richiesta maggiore della quantita\' disponibile.')
            }
        
        # Controllo se la quantità richiesta è maggiore della quantità massima
        if quantity_to_subtract > max_qta:
            return {
                'statusCode': 400,
                'body': json.dumps('Quantita\' richiesta maggiore della quantita\' consentita.')
            }
        
        # Calcolo della nuova quantità dopo la sottrazione
        new_quantity = current_quantity - quantity_to_subtract
        
        # Aggiornamento dell'item nel database con la nuova quantità
        table.update_item(
            Key={'Id': post_id},
            UpdateExpression='SET quantity = :q, lastQuantityBooked = :lqb',
            ExpressionAttributeValues={':q': new_quantity, ':lqb': quantity_to_subtract}
        )
        
        # Restituzione di una risposta di successo
        return {
            'statusCode': 200,
            'body': json.dumps('Prenotazione effettuata con successo.')
        }
    except Exception as e:
        # Restituzione di un errore generico se si verifica un'eccezione
        return {
            'statusCode': 500,
            'body': json.dumps('Errore durante l\'aggiornamento della quantita\' disponibile' )
        }
