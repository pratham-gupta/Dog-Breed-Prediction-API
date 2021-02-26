from django.shortcuts import render
import requests
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response 
import json 
from rest_framework.views import APIView
from api.serializers import  ImageSerializer, Base64ImageSerializer
from PIL import Image
from api.models import UploadImage
import torch
from torchvision import transforms
import pickle
from django.conf import settings
import os
import base64
from datetime import datetime
BASE_DIR = settings.BASE_DIR
MEDIA_ROOT = settings.MEDIA_ROOT


#inference transformation
inference_transformer = transforms.Compose([
                        transforms.Resize((224,224)),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                 std=[0.229, 0.224, 0.225])
])
mapping_file_path = os.path.join(BASE_DIR,'api','code_to_breed.pickle')
with open(mapping_file_path,'rb') as f:
    code_to_breed = pickle.load(f)

#load model
model_file_path = os.path.join(BASE_DIR,'api','complete_model.pt')
model = torch.load(model_file_path,map_location='cpu')





#pytorch inference
def run_inference(model,image_path,inference_transformer,code_to_breed):
    model.eval()
    image = Image.open(image_path)
    transformed_image = inference_transformer(image)
    if torch.cuda.is_available():
        model = model.cuda()
        transformed_image = transformed_image.cuda()
    transformed_image = transformed_image.unsqueeze(0)
    output = model(transformed_image).cpu()
    score,pred = torch.max(output,1)
    print(code_to_breed)
    print(output)
    print(pred)

    return score.data[0], code_to_breed[int(pred.cpu())]
    




# Create your views here.


def prepare_path(BASE_DIR,image_path):
    final_path = os.path.join(BASE_DIR,'dog_breed')
    image_path = image_path.split("/")
    for pt in image_path:
        final_path = os.path.join(final_path,pt)
    return final_path



class ImageView(APIView):
    parser_classes = [MultiPartParser,FormParser]
    
    serializer_class = ImageSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            image = serializer.data.get('image')
            try:
                image_path = prepare_path(BASE_DIR,image)
            except:
                 return Response({"Bad Request":"Invalid Image"},status=status.HTTP_400_BAD_REQUEST)

       
            score, pred = run_inference(model,image_path,inference_transformer,code_to_breed)
            print(score,pred)
            return Response({"Score":score, "Prediction":pred},status=status.HTTP_200_OK)
        return Response({"Bad Request":"Invalid Image"},status=status.HTTP_400_BAD_REQUEST)



class Base64ImageView(APIView):
    # parser_classes = [MultiPartParser,FormParser]
    serializer_class = Base64ImageSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            image_string = serializer.data.get('base64string')
            image_string = bytes(image_string,'utf-8')
            image = base64.decodestring(image_string)
            name = datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '.jpg'
            image_path = os.path.join(MEDIA_ROOT,'images',name)

            with open(image_path,'wb') as f:
                f.write(image)
            


            score, pred = run_inference(model,image_path,inference_transformer,code_to_breed)
            print(score,pred)
            return Response({"Score":score, "Prediction":pred},status=status.HTTP_200_OK)
            
        return Response({"Bad Request":"Invalid Image"},status=status.HTTP_400_BAD_REQUEST)


