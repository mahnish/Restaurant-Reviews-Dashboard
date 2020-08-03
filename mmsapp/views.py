from django.shortcuts import render
from django.http import HttpResponse
import firebase_admin
from firebase_admin import firestore, credentials
from random import randint
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import re
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import urllib.request


def index(request):
	rname="None"
	review1=""
	review2=""
	review3=""
	review4=""
	review5=""
	image1=''
	image2=''
	image3=''
	positive=0
	negative=0
	neutral=0
	predictior=['','','','','']
	if request.method == 'POST':
		rname=request.POST.get('restaurant')
		if rname != None:

			#key for firebase connection
			key = {
			  "type": "service_account",
			  "project_id": "final-project-a9173",
			  "private_key_id": "a056c83499bfb12769100bdfaf2b6b8b61fb9e1c",
			  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCYF1G2WIBiLPgT\nBF9diX4XmK4bjJAqpl45skLPJizHYzQhOh6WRSz68QucC4TGqKEJS5MWFNSWmuWg\n+DUK2lmPtc+6gEAqPP8NJSOWTRxN9bfNISE9/DuVvTQlaJF/tecdRm8k7zyME6Yh\nPbX1OUH/Cmo8GGrTze79kmNSETSzxfJiwC5X7mAwIHAnAoIulOd2tiTlcYOUmHzX\n729Zi10wyqSxOqwUbA62RXZ0zIxVVUrxBkOrPCiCGTQHcXNaKr0tB6h9qx0SvpXx\naHEp5yHhgfWuYD1ctGFzz9bvqcIlL77vpmDJLkB286AOco6pTZ96fAp1h7RMUEJi\n0ikrPgYnAgMBAAECggEAL7fRSVbHIQZe5wiOKzjCOQEMT1RwvxDnq06Eq52cmwpD\nBtHHWvplPG54aAMtK28o51Ow2FK8yGvc8/4sFjWft/khLbCjcR0mIKewXK3g3Yzk\nmBV26o3C3B46yCngzKLz2jmJEZuF8aUQkIleF4xZan2IC0bV7ZJFE4XkZ5FCacyL\ndKcTBWkf1LtZNrd5dTDruxPTtIcrn++Aco8zYxU/XUD20QDYZo/pEojP9iIWWuRC\nBcPv5BAUOeYbHPKoTr1xJyG9Lu0xjNR3uACsUavnYeKXXH286Bp2We+2rx0jOPkx\nCgGcsMQ8QwXQobBEdx1t+xXznbFBTASIv7XwF+mskQKBgQDMY68AiokljkR1oNXG\nrteCC0oDBhmGgzniSYu0nJr0cr1V11SmP3916xnc2SFOUxy2cKHgzDmYYzmmd87k\nWbd4AKjJb3W0uHiBio4oks62OvoCTFbbjjcd4NZs2uw9lPkaA5/fbHAKWBTXepRL\nLONCCyfHTOmcFLmPM1ktx8DoqwKBgQC+fuxuHR/XYabRMFW3VRS1xd2knpeOnwnJ\n3bOPe5FiT9bTRXjXpihWVEXWuf8zMJPnK5ULsfc6z/wmnDAGx5sjDYINL/5fPSPi\nfubHjXTJmhsrsad06DgcM6e1caVCwB3Rh0VLkqpgwlb7R+LeRiJW9FKPdSZ2E0+f\n+/hf1psQdQKBgHyCrXVy76GFTYcq95AVqwt5vRiieqJLBtQnYYghbvRDgbvtdY/h\nVtCK7DJxw6xnTTKG4taDEwMWT2Rt0Aej7/SW0jwEPnxddGvV8EwfQvYYb30+7BrM\nRB9bfMTLiObq/eUvGBGPiaGDjw7FidlR+w+cpBrxa869gV0PNuCAs7AJAoGAVuMF\na+QU1eRQdjGZpxlDbPVm9uLvNboMeOqKL/OoiDLqRUr2p0W+OEIP6LTFVc/eZh5W\nyRLPNSAQXnv22+DHPeG3Y9R0LXRxnalMEdDPZ/TGV9OcEZKppRNad0PyoNOHxj3w\nuVuYIrIBgnNzYvaSSx79WTmR5WFBfDMtQmlcKNECgYEAxBVmggdK2VnlxdXcYECn\nFF9Ed3cbbCudvq7h5gZXzrFPmzv6pe2J9nWvuj/jbTQ+bC0yup2VsG/NNf/PnMgJ\nmXQ4d+HG8exyfcfhLl2kRdex2hqP/o+yAvqU375q7t8qrA/mw6vbqETwvMqPc89n\nmIWPu3WzWX89pZyFGgUlp6k=\n-----END PRIVATE KEY-----\n",
			  "client_email": "firebase-adminsdk-raxg9@final-project-a9173.iam.gserviceaccount.com",
			  "client_id": "112744445966750576723",
			  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
			  "token_uri": "https://oauth2.googleapis.com/token",
			  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
			  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-raxg9%40final-project-a9173.iam.gserviceaccount.com"
			}

			if (not len(firebase_admin._apps)):
			    cred = credentials.Certificate(key) 
			    default_app = firebase_admin.initialize_app(cred)
			db=firestore.client()

			doc_ref=db.collection(rname).document(u'reviews')
			try:
			    doc = doc_ref.get()
			    data=doc.to_dict()
			    #print(u'Document data: {}'.format(doc.to_dict()))
			except google.cloud.exceptions.NotFound:
			    print(u'No such document!')

			index=[]
			for i in range(0,8):
				length=len(data)-2
				randomno=randint(0,length)
				if randomno in index:
					continue
				index.append(randomno)	

			review1=data[f"r{index[0]}"]
			review2=data[f"r{index[1]}"]
			review3=data[f"r{index[2]}"]
			review4=data[f"r{index[3]}"]
			review5=data[f"r{index[4]}"]

			if rname == 'Montanas BBQ and Bar':
				image1='https://media-cdn.tripadvisor.com/media/photo-s/19/5e/9d/98/image.jpg'
				image2='https://s3-media0.fl.yelpcdn.com/bphoto/yBwALcoZO-gcaLfgIhouQg/l.jpg'
				image3='https://1.bp.blogspot.com/-pAcrVe8R1rc/XEorF1HTwAI/AAAAAAABuuo/BdrpXbn1Q84J1OVj3ZMfWj5d_iA0PcYUwCLcBGAs/s1600/038.JPG'

			elif rname == 'Milestones Grill and Bar':
				image1='https://media.glassdoor.com/lst2x/323958/milestones-grill-and-bar-office.jpg'
				image2='https://www.milestonesrestaurants.com/content/cara/milestones/en/jcr%3Acontent/root/responsivegrid/categoryteaser_1350243572.img.1024.jpeg'
				image3='https://media-cdn.tripadvisor.com/media/photo-s/07/3e/0a/37/milestones-grill-bar.jpg'

			elif rname == 'Fionn Maccools':
				image1='https://images.otstatic.com/prod/24441652/1/large.jpg'
				image2='https://media-cdn.tripadvisor.com/media/photo-s/11/44/2d/bb/flagship-burger.jpg'
				image3='https://media-cdn.tripadvisor.com/media/photo-s/10/e6/b5/90/fionn-maccools-lloydminster.jpg'

			elif rname == 'Red Lobster':
				image1='https://media-cdn.tripadvisor.com/media/photo-s/0a/c0/1a/52/red-lobster.jpg'
				image2='https://orionmiami.com/wp-content/uploads/2018/07/319-Bayfield-Street-Barrie-2.jpg'
				image3='https://cdn.usarestaurants.info/assets/uploads/b44f7fd7fde49079175831965e797208_-canada-ontario-simcoe-county-barrie-red-lobster-705-728-2401htm.jpg'

			elif rname == 'Baton Rouge Steakhouse and Bar':
				image1='https://media-cdn.tripadvisor.com/media/photo-s/13/ea/73/bf/exterieur.jpg'
				image2='https://media-cdn.tripadvisor.com/media/photo-s/0e/0c/3a/3a/vibrant-bar-area.jpg'
				image3='https://media-cdn.tripadvisor.com/media/photo-s/0a/90/6e/d4/baton-rouge.jpg'

			doc_ref=db.collection(rname).document(u'ratings')
			try:
			    doc = doc_ref.get()
			    data=doc.to_dict()
			    #print(u'Document data: {}'.format(doc.to_dict()))
			except google.cloud.exceptions.NotFound:
			    print(u'No such document!')

			print(data)
			data.pop("r")
			#print(data['r1']['compound'])
			pos=0
			neg=0
			neu=0
			for i in range(len(data)-1):
				compound=data[f"r{i}"]["compound"]
				
				if compound >= 0.05: 
					pos=pos+1
				elif compound <= - 0.05 : 
					neg=neg+1
				else : 
					neu=neu+1 

			total=pos+neg+neu
			positive=pos/total *100
			neutral=neu/total *100
			negative=neg/total *100
			print(positive)

	if request.method == "POST" and request.POST.get('restaurant') == None:

		myfile = request.FILES['myfile']

		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		print(filename)

		ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"

		# Replace with a valid key
		prediction_key = "afc53c5c11d24d90a6b573903798674b"
		prediction_resource_id = "/subscriptions/33ed2130-f2e8-4465-8b37-ee0b4fb43621/resourceGroups/SocialData/providers/Microsoft.CognitiveServices/accounts/SocialData"

		publish_iteration_name = "FinalApp"

		project="FinalApp"
		project_id="b2a087a8-b1a2-4c95-8758-038b3a56eb57"


		# Now there is a trained endpoint that can be used to make a prediction
		prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
		predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

		with open(filename, "rb") as image_contents:
		    results = predictor.classify_image(
		    project_id, publish_iteration_name, image_contents.read())

		predictior=[]
		# Display the results.
		for prediction in results.predictions:
		    predictior.append(prediction.tag_name +
		          ": {0:.2f}%".format(prediction.probability * 100))



	return render (request, "mmsapp/dashboard.html" , context={
		'name':rname,
		'review1':review1,
		'review2':review2,
		'review3':review3,
		'review4':review4,
		'review5':review5,
		'image1': image1,
		'image2':image2,
		'image3':image3,
		'positive':positive,
		'negative':negative,
		'neutral':neutral,
		'p0': predictior[0],
		'p1': predictior[1],
		'p2': predictior[2],
		'p3': predictior[3],
		'p4': predictior[4]
		})
