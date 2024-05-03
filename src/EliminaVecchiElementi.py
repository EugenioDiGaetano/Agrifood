import json
import boto3
from datetime import datetime, timedelta

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

        # Calcola la data e l'ora attuale meno una settimana
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Formatta la data nel formato richiesto per DynamoDB
        cutoff_date = one_week_ago.strftime('%Y-%m-%d')
        
        # Interroga la tabella per recuperare gli elementi inseriti prima della data di cutoff
        response = table.scan(
            FilterExpression='#dt < :cutoff_date',
            ExpressionAttributeNames={'#dt': 'date'},  # Utilizza un alias per l'attributo "date"
            ExpressionAttributeValues={':cutoff_date': cutoff_date}
        )

        
        # Ottieni gli elementi trovati
        items_to_delete = response.get('Items', [])
        
        # Elimina gli elementi trovati
        for item in items_to_delete:
            post_id = item.get('Id')
            table.delete_item(Key={'Id': post_id})
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"{len(items_to_delete)} elementi eliminati.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Errore durante l'eliminazione degli elementi: {str(e)}")
        }
