import json
import boto3

# Crea un client per AWS Systems Manager Parameter Store
ssm_client = boto3.client('ssm')

# Inizializza il client DynamoDB
dynamodb = boto3.client('dynamodb')

# Nome del parametro che contiene il nome della tabella
parameter_name = '/TableName'

def get_all_items_from_db():

    try:
        # Ottiene il nome della tabella DynamoDB dal parametro
        table_name = ssm_client.get_parameter(Name=parameter_name)['Parameter']['Value']
        
        # Effettua la scansione della tabella e recupera tutti gli elementi
        response = dynamodb.scan(TableName=table_name)

        # Lista per memorizzare gli elementi filtrati
        filtered_items = []

        # Per ogni elemento, escludi il campo "password" e aggiungi l'elemento filtrato alla lista
        for item in response['Items']:
            filtered_item = {key: value for key, value in item.items() if key.lower() != 'password'}
            filtered_items.append(filtered_item)

        # Restituisci la lista degli elementi filtrati
        return filtered_items
    except Exception as e:
        # In caso di errore, restituisci un dizionario contenente un messaggio di errore
        raise ValueError(f"Errore durante il recupero degli elementi dalla tabella DynamoDB: {str(e)}")

def lambda_handler(event, context):

    try:
        # Ottiene tutti gli elementi dalla tabella DynamoDB
        all_items = get_all_items_from_db()
        return {
            'statusCode': 200,
            'body': json.dumps(all_items)
        }
    except ValueError as ve:
        # In caso di errore, restituisce un messaggio di errore
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(ve)})
        }
    except Exception as e:
        # In caso di eccezione generica, restituisce un messaggio di errore generico
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Errore interno del server: {str(e)}"})
        }
