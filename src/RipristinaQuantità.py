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
        
        # Scansione della tabella per recuperare tutti i post con quantità pari a zero
        response = table.scan(
            FilterExpression='#q = :zero',
            ExpressionAttributeNames={'#q': 'quantity'},  # Utilizza un alias per l'attributo "quantity"
            ExpressionAttributeValues={':zero': 0}
        )

        # Ottieni gli elementi trovati
        items_to_update = response.get('Items', [])
        
        # Aggiorna gli elementi trovati
        for item in items_to_update:
            post_id = item.get('Id')
            last_quantity_booked = item.get('lastQuantityBooked', 0)  # Assume che ci sia un attributo "lastQuantityBooked"
            
            # Aggiorna la quantità del post con il valore dell'ultima quantità prenotata
            table.update_item(
                Key={'Id': post_id},
                UpdateExpression='SET quantity = :q',
                ExpressionAttributeValues={':q': last_quantity_booked}
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"{len(items_to_update)} elementi aggiornati.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Errore durante l'aggiornamento degli elementi: {str(e)}")
        }
