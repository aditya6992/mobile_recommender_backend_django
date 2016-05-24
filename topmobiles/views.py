from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from models import Mobile
from serializers import mobileSerializer

@csrf_exempt
@api_view(['GET','POST'])
def mobiles(request):
    #connect to our local mongodb
    client = MongoClient('localhost',27017)
    #get a connection to our database
    db = client['gsmarena']
    mobileCollection = db['phones_test']

    if request.method == 'GET':
        #get our collection
        mobiles = []
        camera = int(request.query_params['camera'])
        ram = int(request.query_params['ram'])
        storage = int(request.query_params['storage'])
        battery = int(request.query_params['battery'])
        list1 = mobileCollection.find()
        newlist = sorted(list1, key=lambda k: ((camera * int(k['camera']))/8) + ((battery * int(k['battery']))/2100) +
                                              ((ram * int(k['ram']))/2) + ((storage * int(k['storage']))/8),
                         reverse=True)
        for r in newlist:
            mobile = Mobile(r["url"],r["name"],r["camera"],r["ram"],r["storage"],r["battery"])
            mobiles.append(mobile)
        serializedList = mobileSerializer(mobiles, many=True)
        # print serializedList
        return Response(serializedList.data)
    elif request.method == 'POST':
        pass