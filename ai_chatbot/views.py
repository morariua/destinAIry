import json
from typing import re

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .shared_keys import MAX_CHAR_INPUT, INPUT_EXCEEDED_MESSAGE, OPENAI_CHAT_MODEL
from . import langllamaSetup
from .usefulFunc import num_tokens_from_string
from .utils import setup_chatgpt

from rest_framework.decorators import api_view, authentication_classes,\
permission_classes
#from rest_framework.authentication import TokenAuthentication
## use BasicAuthentication instead of TokenAuthentication. 
#BasicAuthentication allows you to specify a single API key that can be used by all users.
from rest_framework.authentication import BasicAuthentication
#from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils import SecretKeyGenerator
from rest_framework import status
from .models import ApiKey
from .serializers import ApiKeySerializer

from rest_framework import viewsets, mixins

# Create your views here.
###setup_chatgpt()

class ApiKeyViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin):
    """Handles Creating API keys"""
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated] ##, IsAdminUser]
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer

    '''
    Additional info:
    ## lookup_value_regex = '[\w]+' ## to allow only alphanumeric characters (1 or more)
    lookup_value_regex is not a valid attribute in the ModelViewSet or GenericViewSet classes,
    which are the parent classes of ApiKeyViewSet. However, you can override the 
    lookup_field attribute to change the field that is used to look up objects in the retrieve() method.
    '''
    '''
    a view that allows users to generate a single API key, and 
    clicking the "Generate" button will delete the previous key 
    (if it exists) and create a new one:
    '''
    def api_key(request):
        try:
            api_key = ApiKey.objects.get(id=1)
        except ApiKey.DoesNotExist:
            api_key = None

        if request.method == 'POST':
            # Delete the current API key (if it exists)
            if api_key:
                api_key.delete()

            # Generate a new API key
            key = SecretKeyGenerator.generate_secret_key() # get_random_string(length=40)
            api_key = ApiKey.objects.create(id=1, key=key)

        context = {'api_key': api_key.key if api_key else None}
        return render(request, 'api_key.html', context)





@api_view(http_method_names=['GET','POST']) #,'DELETE'])
@authentication_classes([BasicAuthentication])
#@permission_classes([IsAuthenticated]) ## NOT NEEDED for BasicAuthentication
@csrf_exempt
def view_API(request): ## do not need to use APIView parent class 
    #(from rest_framework.views) if @api_view is used.
    #See https://stackoverflow.com/questions/53276279/how-to-add-tokenauthentication-authentication-classes-to-django-fbv
    '''
    below is not needed if you already give the annotation above
    and if below is just a function & NOT a viewset class!
    '''
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    # Check if authentication key is valid
    key = request.META.get('HTTP_AUTHORIZATION') ## Retrieve your-api-key with 
    # curl requests in the format of: 'curl -H "Authorization: <your-api-key>"'
    try:
        api_key = ApiKey.objects.get(key=key)
    except TypeError as e: ## as accessing "/api/" without an authentication key provides a "key is None" TypeError
        return Response({'message': 'No authentication key was passed'}, status=status.HTTP_403_FORBIDDEN)
    except ApiKey.DoesNotExist as e:
        return Response({'message': 'Invalid authentication key'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        my_apikeys = ApiKey.objects.all()
        my_serializer = ApiKeySerializer(my_apikeys, many=True)
        return Response(my_serializer.data)
    if request.method == "POST":
        # print(f"request.body: {request.body}")
        ## Decode the request body from bytes to string
        b0dy = request.body.decode('utf-8')
        # print(f"b0dy: {b0dy}")
        ## Parse the JSON string into a Python dictionary
        python_dict_c0ntent = json.loads(b0dy)
        # print(f"python_dict_c0ntent: {python_dict_c0ntent}")
        ## Access the 'questi0n' value from the parsed data
        question = python_dict_c0ntent.get("questi0n", "")
        num_tokens_from_string(question, OPENAI_CHAT_MODEL, "---QUESTION")
        # print(f"question: {question}")
        if len(question) > int(MAX_CHAR_INPUT):
            res = {'answer': INPUT_EXCEEDED_MESSAGE}
            return JsonResponse(res)
        try:
            response = langllamaSetup.agentExecutor_DestinAIry.run(input=question.replace('\n', ' ')).strip().replace('\n', '<br>')
        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: "):
                raise e
            response = response.removeprefix("Could not parse LLM output: ").removesuffix("`").strip()
        num_tokens_from_string(response, OPENAI_CHAT_MODEL, "---RESPONSE")
        #### GET CSV OUTPUT
        csv_output = response.split("```")[1]
        #### CONVERTING CSV TO JSON
        # Split the string into rows
        rows = csv_output.split('\n')
        # Split each row into columns
        columns = [row.split(',') for row in rows]
        # Create a DataFrame from the columns
        df = pd.DataFrame(columns[1:], columns=columns[0])

        # Convert the DataFrame to a JSON object
        json = df.to_json(orient='records')
        response = json.loads(action.strip())
        res = {}
        res['answer'] = response
        return JsonResponse(res)


## UI VIEW
@csrf_exempt ## Note: disable CSRF protection for Django app use as local API use
def view_UI(request):
    if request.method == "POST":
        question = request.POST.get("questi0n", "")
        num_tokens_from_string(question, OPENAI_CHAT_MODEL, "---QUESTION")
        if len(question) > int(MAX_CHAR_INPUT):
            res = {}
            res['answer'] = INPUT_EXCEEDED_MESSAGE
            return JsonResponse(res)
        # response = langllamaSetup.agentExecutor_DestinAIry.run(input=question.replace('\n', ' ')).strip().replace('\n', '<br>')
        from .chatTempl import chat_prompt
        print(f"chat_prompt: {chat_prompt}")
        response = chat_prompt.format()
        print(f"response: {response}")
        # try:
        #     if response.__contains__("None"):
        #         response = "Sorry, I do not have the answer to your question."
        # except ValueError as e:
        #     response = str(e)
        #     if not response.startswith("Could not parse LLM output: "):
        #         raise e
        #     response = response.removeprefix("Could not parse LLM output: ").removesuffix("`").strip()
        # num_tokens_from_string(response, OPENAI_CHAT_MODEL, "---RESPONSE")
        # itinerary_match = re.search(r"```(.*?)```?", response, re.DOTALL)
        # if itinerary_match is not None:
        #     text = json.loads(itinerary_match.group(1).strip(), strict=False)
        # # Remove leading and trailing spaces from column names
        # text_formatted = text.replace('"', '')
        # columns = [col.strip() for col in text_formatted.split('\n')[0].split(',')]
        # print(f"columns: {columns}")
        # # Split the string into rows
        # rows = [row.strip().split(',') for row in text_formatted.split('\n')[1:]]
        # print(f"rows: {rows}")
        # # Create a DataFrame from the columns
        # df = pd.DataFrame(rows, columns=columns).replace('"', '', regex=True)
        #
        # # Set the date column as the index
        # df.set_index('date', inplace=False) ## if True, date column will disappear
        #
        # # Convert the DataFrame to a JSON object
        # json_output = df.to_json(orient='records')
        #
        # # Print the JSON object
        # print(json_output)
        #
        # res = {}
        # res['answer'] = rows
        # print(f"\n\nr0ws: {rows}")
        # return JsonResponse(res)
    return render(request, 'chatb0t.html')


## View function for error.html page
def error_403(request, exception):
    return render(request, 'nopermission.html', status=403)