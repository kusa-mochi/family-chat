import boto3
import json

dynamodb = boto3.resource('dynamodb')
connectionsTable = dynamodb.Table('family-chat-connections')

def lambda_handler(event, context):
    print('sendChat start.')
    
    #########################

    postData = json.loads(event.get('body', '{}')).get('data')
    token = postData['token']
    message = postData['message']
    
     # トークンの検証
    token = postData['token']
    connection = connectionsTable.get_item(Key={'token': token})
    # if a token is not exist on DB
    if token != connection['Item']['token']:
        return {
            'statusCode': 404,
            'body': json.dumps('access denied.')
        }
    
    #########################
    
    senderName = connectionsTable.get_item(Key={'token': token})['Item']['userName']
    
    #########################
    
    connections = connectionsTable.scan().get('Items')
    if connections is None:
        return {
            'statusCode': '404',
            'body': json.dumps('404')
        }
    
    for connection in connections:
        am = boto3.client('apigatewaymanagementapi', endpoint_url=connection['endpointUrl'])
        _ = am.post_to_connection(ConnectionId=connection['connectionId'], Data=json.dumps({
            'dataType': 'receivedChat',
            'data': {
                'message': message,
                'userName': senderName
            }
        }))
    
    #########################
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
