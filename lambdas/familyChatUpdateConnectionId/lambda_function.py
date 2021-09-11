import boto3
import json

dynamodb = boto3.resource('dynamodb')
connectionsTable = dynamodb.Table('family-chat-connections')

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
    
    # 更新した旨をクライアントに返信する。
    am = boto3.client('apigatewaymanagementapi', endpoint_url=endpointUrl)
    _ = am.post_to_connection(ConnectionId=connectionId, Data=json.dumps({
        'dataType': 'updatedConnectionId'
    }))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
