from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Clients, Montants_Abonnements, AbonneClient
from rest_framework.views import APIView
from Client.ClientSerializers import ClientEseSerializer, Montants_AbonnementsSerializer, AbonneClientSerializer
from .pwd_generator import CodeGenerator, PwdGenerator, codeabonnement, abonnement
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import datetime

# Create your views here.


class ClientViewSet(ModelViewSet):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Clients.objects.all()
    serializer_class = ClientEseSerializer

    def get_serializer_context(self):
        return {'request': self.request,}
    
    def perform_create(self, serializer):
        
        # code = CodeGenerator()
        mdpbrut = PwdGenerator()
        abnment = codeabonnement()
        serializer.save(mdp_admin=mdpbrut, code_ab=abnment)

        return Response(serializer.data, status=status.HTTP_200_OK)



class MontAbonViews(ModelViewSet):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Montants_Abonnements.objects.all()
    serializer_class = Montants_AbonnementsSerializer



class ClientAbonneViewset(ModelViewSet):
    parser_classes = [FormParser, MultiPartParser]
    queryset = AbonneClient.objects.all()
    serializer_class = AbonneClientSerializer

    def perform_create(self, serializer):
        data = self.request.data
        
        client = Clients.objects.filter(id_enreg= data['ese']).first() 
        
        if client == None :
            return Response({
                'status': False,
                'message': "Nom d'entreprise inexistante"
            }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            
            racine = abonnement()
            dat = str(datetime.date.today())
            print(dat)
            d = dat[9:]
            m = dat[6:8]               
            ab = str(client.code_ab)+d+m+str(racine)
            # data["num_abon"] = ab
        
            code = CodeGenerator()
            serializer.save(code=code, num_abon=ab, schema_name=client.schema_name)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        