import json
from csv import DictReader
import re
from .openaiSetup import generate_response

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .shared_keys import MAX_CHAR_INPUT, INPUT_EXCEEDED_MESSAGE, OPENAI_CHAT_MODEL
from .usefulFunc import num_tokens_from_string

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
<<<<<<< HEAD
             last_name = python_dict_c0ntent.get("last_name", "NULL")
             nationality = python_dict_c0ntent.get("nationality", "NULL")
             age = python_dict_c0ntent.get("age", "NULL")
             first_name = python_dict_c0ntent.get("first_name", "NULL")
             gender = python_dict_c0ntent.get("gender", "NULL")
             destinations = python_dict_c0ntent.get("destinations", "NULL")
             duration = python_dict_c0ntent.get("duration", "NULL")
             start_date = python_dict_c0ntent.get("start_date", "NULL")
             response = generate_response(text=question, first_name=first_name, last_name=last_name, nationality=nationality,
                                          age=age, gender=gender, destinations=destinations, duration=duration,
                                          start_date=start_date)
        except Exception as e:
             print (f"EXCEPTION OCCURRED: {e}")
             res = {'answer': "Sorry, some details were missing in your prompt. Please try again."}
             return JsonResponse(res)
        print(f"response: {response}\n\n\n")
        content = response.content
        #content = 'I suggest the following itinerary for your 1-day trip to Mongolia on July 1, 2023:' \
          #        '```\n' \
           #       '"date","name","addr","pop","hrs","mode","cost","remark","type"\n' \
            #      '"2023-07-01","Gandantegchinlen Monastery","Gandantegchinlen Khiid","90","2.5","TX","0","Buddhist monastery with impressive statue of Avalokitesvara","POI"\n' \
             ##    '```' \
               #   'The first place is Gandantegchinlen Monastery, a beautiful Buddhist monastery with an im' \
                #  'pressive statue of Avalokitesvara. The second place is Gorkhi-Terelj National Park, a national park with scenic views and hiking trails. Both places are best reached by car and are highly popular tourist destinations. This itinerary should give you a great taste of Mongolias culture and natural beauty in just one day.'
=======
            first_name = python_dict_c0ntent.get("first_name", "NULL")
            last_name = python_dict_c0ntent.get("last_name", "NULL")
            nationality = python_dict_c0ntent.get("nationality", "NULL")
            age = python_dict_c0ntent.get("age", "NULL")
            gender = python_dict_c0ntent.get("gender", "NULL")
            destinations = python_dict_c0ntent.get("destinations", "NULL")
            duration = python_dict_c0ntent.get("duration", "NULL")
            start_date = python_dict_c0ntent.get("start_date", "NULL")
            response = generate_response(text=question, first_name=first_name, last_name=last_name, nationality=nationality,
                                        age=age, gender=gender, destinations=destinations, duration=duration,
                                        start_date=start_date)
        except Exception as e:
            print (f"EXCEPTION OCCURRED: {e}")
            res = {'answer': "Sorry, some details were missing in your prompt. Please try again."}
            return JsonResponse(res)
        print(f"response: {response}\n\n\n")
        content = response.content
        #content = 'I suggest the following itinerary for your 1-day trip to Mongolia on July 1, 2023:' \
        #          '```\n' \
        #          '"date","name","addr","pop","hrs","mode","cost","remark","type"\n' \
        #          '"2023-07-01","Gandantegchinlen Monastery","Gandantegchinlen Khiid","90","2.5","TX","0","Buddhist monastery with impressive statue of Avalokitesvara","POI"\n' \
        #          '"2023-07-01","Gorkhi-Terelj National Park","Gorkhi-Terelj National Park","85","3","TX","0","National park with scenic views and hiking trails","POI"' \
        #          '```' \
        #          'The first place is Gandantegchinlen Monastery, a beautiful Buddhist monastery with an im' \
        #          'pressive statue of Avalokitesvara. The second place is Gorkhi-Terelj National Park, a national park with scenic views and hiking trails. Both places are best reached by car and are highly popular tourist destinations. This itinerary should give you a great taste of Mongolias culture and natural beauty in just one day.'
>>>>>>> 6f52943271746178ec5bc2b3df1998ddf7f4bf42
        print(f"content: {content}\n\n\n")
        num_tokens_from_string(content, OPENAI_CHAT_MODEL, "---RESPONSE")
        itinerary_match = re.search(r"```(.*?)```?", content, re.DOTALL)
        if itinerary_match is not None:  ## if an itinerary was suggested
            print(f"\n\n\nITINERARY_DETECTED==========")
            ## Extract the itinerary, and convert it into a JSON object
            text = itinerary_match.group(1).strip()
            rows = []
            for row in DictReader(text.splitlines(), delimiter=',', quotechar='"'):
                rows.append(row)
            df = pd.DataFrame(rows)
            # Remove any double quotes from all columns
            df = df.applymap(lambda x: x.replace('"', '') if isinstance(x, str) else x)
            # Set the date column as the index
            df.set_index('date', inplace=False)
            # Convert the DataFrame to a JSON object
            json_output = df.to_json(orient='records')
            # Print the JSON object
            print(f"\n\njson_output: {json_output}\n\n")
            ## Extract out the text outside the itinerary
            pattern = re.compile(r'^((?:(?!```)[\s\S])+)[\s\S]*```[\s\S]*```')
            match = re.search(pattern, content)
            pattern_2 = r'```([^`]*)$'
            match_2 = re.search(pattern_2, content, re.DOTALL)
            if match or match_2:
                response = match.group(1).strip().replace(":", ".\n\n") + match_2.group(1).strip()
                print(f"MATCHED_GROUP: {response}")
            else:
                response = "Thank you for your suggestions. I have came up with the best itinerary I can for you."
            res = {'answer': response, 'data': json_output}
            return JsonResponse(res)
        ## Else just return AI response which is to ask for more questions
        res = {'answer': content}
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
        response = generate_response(text=question, first_name="casey", last_name="vo", nationality="viet",
                                                age="21", gender="female", destinations="paris", duration="1 day", start_date="june1,2023")
        print(f"response: {response}\n\n\n")
        content = response.content
#         content = """Great! Based on your preferences, here's an itinerary for your one-day trip to Shanghai:
# ```
# "date","name","addr","pop","hrs","mode","cost","remark","type"
# "2022/11/01","Grand Mercure Shanghai Century Park","1199 Yingchun Road, Pudong New Area","90","NA","NA","500","Wheelchair-friendly hotel near Century Park","ACC"
# "2022/11/01","Century Park","Huamu Road","85","2","WK","0","Large park with lake, gardens and sports facilities","POI"
# "2022/11/01","Shanghai Tower","501 Yincheng Middle Road, Lujiazui, Pudong New Area","95","3","TX","150","Tallest building in China with observation deck","POI"
# "2022/11/01","Nanjing Road Pedestrian Street","Nanjing Road","90","2","WK","0","Famous shopping street with cafes and restaurants","POI"
# "2022/11/01","Tianzifang","Lane 210, Taikang Road, Luwan District","80","2","WK","0","Artistic alleyways with cafes and shops","POI"
# "2022/11/01","Yu Garden","218 Anren Street, Huangpu District","85","2","WK","40","Classical Chinese garden with tea house","POI"
# "2022/11/01","Hengshan Road","Hengshan Road","80","2","WK","0","Tree-lined street with cafes and bars","POI"
# "2022/11/01","Xintiandi","Lane 181, Taicang Road, Luwan District","85","2","WK","0","Historic shikumen buildings with cafes and shops","POI"
# "2022/11/01","Jade Buddha Temple","170 Anyuan Road, Putuo District","85","2","WK","50","Buddhist temple with jade Buddha statues","POI"
# "2022/11/01","Wheelock Square","1717 Nanjing West Road, Jing'an District","80","2","WK","0","Modern shopping mall with cafes and restaurants","POI"
# ```
# You will be staying at the Grand Mercure Shanghai Century Park, a wheelchair-friendly hotel near Century Park. On your first day, you can visit Century Park, the largest park in Shanghai, and then head
#         """
        print(f"content: {content}\n\n\n")
        num_tokens_from_string(content, OPENAI_CHAT_MODEL, "---RESPONSE")
        itinerary_match = re.search(r"```(.*?)```?", content, re.DOTALL)
        print(f"itinerary_match: {itinerary_match.group(1)}")
        if itinerary_match is not None: ## if an itinerary was suggested
            print(f"\n\n\nITINERARY_DETECTED==========")
            ## Extract the itinerary, and convert it into a JSON object
            text = itinerary_match.group(1).strip()
            rows = []
            for row in DictReader(text.splitlines(), delimiter=',', quotechar='"'):
                rows.append(row)
            df = pd.DataFrame(rows)
            # Remove any double quotes from all columns
            df = df.applymap(lambda x: x.replace('"', '') if isinstance(x, str) else x)
            # Set the date column as the index
            df.set_index('date', inplace=False)
            # Convert the DataFrame to a JSON object
            json_output = df.to_json(orient='records')
            # Print the JSON object
            print(f"\n\njson_output: {json_output}\n\n")
            ## Extract out the text outside the itinerary
            pattern = re.compile(r'^((?:(?!```)[\s\S])+)[\s\S]*```[\s\S]*```')
            match = re.search(pattern, content)
            pattern_2 = r'```([^`]*)$'
            match_2 = re.search(pattern_2, content, re.DOTALL)
            if match or match_2:
                response = match.group(1).strip().replace(":", ".\n\n") + match_2.group(1).strip()
                print(f"MATCHED_GROUP: {response}")
            else:
                response = "Thank you for your suggestions. I have came up with the best itinerary I can for you."
            res = {'answer': response, 'data': json_output}
            return JsonResponse(res)
        ## Else just return AI response which is to ask for more questions
        res = {'answer': content}
        return JsonResponse(res)
    return render(request, 'chatb0t.html')


## View function for error.html page
def error_403(request, exception):
    return render(request, 'nopermission.html', status=403)