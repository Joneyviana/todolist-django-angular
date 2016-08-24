from django.shortcuts import render

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.conf import settings


class AuthorizeView(APIView):

    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)

    access_token_url = 'https://graph.facebook.com/v2.3/oauth/access_token'
    graph_api_url = 'https://graph.facebook.com/v2.5/me?fields=id,email'
    
    def post(self, request, format=None):
        params = {
        'client_id': request.data['clientId'],
        'redirect_uri': request.data['redirectUri'],
        'client_secret':settings.FACEBOOK_SECRET,
        'code': request.data['code']
        }
        r = requests.get(access_token_url, params=params)
        # use json.loads instad of urlparse.parse_qsl
        access_token = json.loads(r.text)

        # Step 2. Retrieve information about the current user.
        r = requests.get(graph_api_url, params=access_token)
        profile = json.loads(r.text)
        try:
            user = User.objects.filter(id=profile['id'])[0]
        except IndexError:
            pass
        import jwt
        from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
        if user:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token.decode('unicode_escape')},
                            status=status.HTTP_200_OK)
        user = User.objects.create(username=profile['name'])
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'Bearer': token.decode('unicode_escape')},
                        status=status.HTTP_200_OK)

        
