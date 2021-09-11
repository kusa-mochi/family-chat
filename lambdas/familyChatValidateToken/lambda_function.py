import boto3
import json

dynamodb = boto3.resource('dynamodb')
connectionsTable = dynamodb.Table('family-chat-connections')

def lambda_handler(event, context):
    print('validateToken start.')
    
    #########################

    postData = json.loads(event.get('body', '{}')).get('data')
    
    # クライアントの宛先情報（WebSocketの接続ID）
    connectionId = event.get('requestContext', {}).get('connectionId')
    
    # クライアントの宛先情報（API GatewayのURL）
    domainName = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    endpointUrl = F"https://{domainName}/{stage}"
    
    #########################
    
    # DynamoDBにトークンが登録されているか確認する。
    response = connectionsTable.get_item(Key={'token': postData['token']})
    am = boto3.client('apigatewaymanagementapi', endpoint_url=endpointUrl)
    if 'Item' in response:
        # トークンが登録されていた場合
        _ = am.post_to_connection(ConnectionId=connectionId, Data=json.dumps({"dataType": "validToken"}))
    else:
        # トークンが登録されていない場合
        _ = am.post_to_connection(ConnectionId=connectionId, Data=json.dumps({"dataType": "invalidToken"}))
    
    return {
        'statusCode': 200,
        'body': json.dumps('validateToken fin.')
    }
