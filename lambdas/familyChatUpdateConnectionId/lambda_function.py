import boto3
import json

dynamodb = boto3.resource('dynamodb')
connectionsTable = dynamodb.Table('family-chat-connections')
logsTable = dynamodb.Table('family-chat-logs')

def lambda_handler(event, context):
    print('updateConnectionId start.')
    
    postData = json.loads(event.get('body', '{}')).get('data')
    
    # トークンの検証
    token = postData['token']
    connection = connectionsTable.get_item(Key={'token': token})
    # if a token is not exist on DB
    if token != connection['Item']['token']:
        return {
            'statusCode': 404,
            'body': json.dumps('access denied.')
        }
    
    # クライアントの宛先情報（WebSocketの接続ID）
    connectionId = event.get('requestContext', {}).get('connectionId')
    
    # クライアントの宛先情報（API GatewayのURL）
    domainName = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    endpointUrl = F"https://{domainName}/{stage}"
    
    # DB上の宛先情報の更新
    connectionsTable.update_item(
        Key={'token': token},
        UpdateExpression='set connectionId=:connectionId,endpointUrl=:endpointUrl',
        ExpressionAttributeValues={
            ':connectionId': connectionId,
            ':endpointUrl': endpointUrl
        },
        ReturnValues='UPDATED_NEW'
        )
    
    # チャットログ
    logs = logsTable.scan().get('Items')
    if logs is None:
        return {
            'statusCode': '200',
            'body': json.dumps('200')
        }
    logsArr = []
    for log in logs:
        logsArr.append({
            'userName': log['userName'],
            'message': log['message'],
            'expirationDatetime': int(log['expirationDatetime'])
        })
    
    # 更新した旨と、現在のチャットログをクライアントに返信する。
    am = boto3.client('apigatewaymanagementapi', endpoint_url=endpointUrl)
    _ = am.post_to_connection(ConnectionId=connectionId, Data=json.dumps({
        'dataType': 'updatedConnectionId',
        'data': {
            'logs': logsArr
        }
    }))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
