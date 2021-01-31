from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from twilio.rest import Client

t_auth_key = '54fb597cae02a4adcda1a08fc0a09044'
account_sid =  'AC08498a1ba4f7c716135afda08dcee6f1'
api_key_sid = 'SK1379d362d263db56d1a8c703576d7032'
api_key_secret ='eag4G67RGdREYMklr4kDnxVtoyGWR2c9'

client = Client(account_sid, t_auth_key)

token = AccessToken(account_sid, api_key_sid,
                            api_key_secret, identity='abc')

room = client.video.rooms('RM1ff35d54cbe8b3a99ccba803e63e2188').fetch()

token.add_grant(VideoGrant(room=room.sid))

print(token.to_jwt())