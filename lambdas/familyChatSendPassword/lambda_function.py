import boto3
import datetime
import hashlib
import json

dynamodb = boto3.resource('dynamodb')
connectionsTable = dynamodb.Table('family-chat-connections')
passwordHashTable = dynamodb.Table('family-chat-passwordhash')

def lambda_handler(event, context):
    print('sendPassword start.')
    
    #########################

    postData = json.loads(event.get('body', '{}')).get('data')
    
    
    # クライアントの宛先情報（WebSocketの接続ID）
    connectionId = event.get('requestContext', {}).get('connectionId')
    
    # クライアントの宛先情報（API GatewayのURL）
    domainName = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    endpointUrl = F"https://{domainName}/{stage}"
    
    #########################
    
    # posted password
    password = postData['password']
    
    # posted user name
    userName = postData['userName']
    
    # posted password hash
    postedPasswordHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    # password hash in DB
    dbPasswordHash = passwordHashTable.get_item(Key={'id': 0})['Item']['hash']
    
    #########################
    
    if postedPasswordHash != dbPasswordHash:
        # return error.
        am = boto3.client('apigatewaymanagementapi', endpoint_url=endpointUrl)
        _ = am.post_to_connection(ConnectionId=connectionId, Data=json.dumps({"dataType":"invalidPassword"}))
        return {
            'statusCode': 404,
            'body': json.dumps('familyChatSendPassword fin.')
        }
    
    #########################
    
    # 現在時刻
    now = datetime.datetime.now()
    nowString = (now.strftime('%Y-%m-%d %H:%M:%S.%f'))
    print(nowString)
    
    # トークンの有効期限
    expirationDatetime = int((now + datetime.timedelta(hours=1)).timestamp())
    
    # 現在時刻から新規にトークンを生成する。トークンは以後の通信でクライアントの識別に用いる。
    token = hashlib.sha256(nowString.encode('utf-8')).hexdigest()
    print(token)
    
    #########################
    
    # トークンとユーザ名を有効期限付でDBに登録する。
    response = connectionsTable.put_item(Item={
        'token': token,
        'userName': userName,
        'expirationDatetime': expirationDatetime,
        'connectionId': connectionId,
        'endpointUrl': endpointUrl
    })
    
    #########################
    
    # クライアントにトークンを送る。
    am = boto3.client('apigatewaymanagementapi', endpoint_url=endpointUrl)
    _ = am.post_to_connection(ConnectionId=connectionId, Data=json.dumps({"dataType":"newToken", "data":{"token": token}}))
    
    #########################
    
    return {
        'statusCode': 200,
        'body': json.dumps('familyChatSendPassword fin.')
    }
