import boto3
import datetime
import json

dynamodb = boto3.resource('dynamodb')
connectionsTable = dynamodb.Table('family-chat-connections')
logsTable = dynamodb.Table('family-chat-logs')

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
    
    # 現在時刻
    now = datetime.datetime.now()
    
    # ログの有効期限（30日間）
    expirationDatetime = int((now + datetime.timedelta(days=30)).timestamp())
    
    # DynamoDBにログを記録する。
    logsTable.put_item(Item={
        'expirationDatetime': expirationDatetime,
        'userName': senderName,
        'message': message
    })
    
    #########################
    
    connections = connectionsTable.scan().get('Items')
    if connections is None:
        return {
            'statusCode': '404',
            'body': json.dumps('404')
        }
    
    for connection in connections:
        try:
            am = boto3.client('apigatewaymanagementapi', endpoint_url=connection['endpointUrl'])
            _ = am.post_to_connection(ConnectionId=connection['connectionId'], Data=json.dumps({
                'dataType': 'receivedChat',
                'data': {
                    'message': message,
                    'userName': senderName
                }
            }))
        except:
            pass
    
    #########################
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
