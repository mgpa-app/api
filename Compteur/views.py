from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from .CompteurSerializer import CompteurSerializer, CompteurCreateSerializer, AlerteEpSerializer, CountCritiqSerializer
from .models import Compteurs, AlerteEp, CountCritique
from rest_framework.viewsets import ModelViewSet
from mgpa.middleware import get_tenant
from django_tenants.utils import tenant_context
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from Matroulant.models import VehiculesEses
from .models import Compteurs
from Mgpausers.models import GlobalUser
from rest_framework import status
from django.db.models import Q
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


User = get_user_model()

class CompteurCreate(ModelViewSet):
    parser_classes = [FormParser, MultiPartParser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["vehicule", "compt_act", "date_compt", "releveur", "ecart", "statut_compt"]
    ordering_fields = ["date_compt"]
    pagination_class = PageNumberPagination
    serializer_class = CompteurSerializer

    def get_queryset(self): 
        users = self.request.user
        return Compteurs.objects.filter(Q(vehicule_id=self.kwargs['engin_pk'])).select_related('vehicule')
        # return VehiculesEses.objects.filter(Q(id=self.kwargs['engin_pk']) & Q(conducteurs__id=self.request.user.id))
        # if users in veh.conducteurs.all():        
        #     return Compteurs.objects.filter(Q(vehicule_id=veh)).select_related('vehicule')
        # else:
        #     return Response("Engin n'appartenant pas")
        
        
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return {"engin_id": self.kwargs['engin_pk']}
    
    def create(self, request, *args, **kwargs):
        type_zone = ["DIR_EXPLOIT", "CHEF_SMRLT"]
        type_total = ["MASTER_DATA", "DIR_GEN"]
        cpt = ''
        usercurrent = self.request.user
        veh = VehiculesEses.objects.get(id=self.kwargs['engin_pk'])

        if usercurrent.type in type_zone:    
            cpt = 'oui'
            
        elif usercurrent.type in type_total:
            cpt = 'oui'
        else:
            idd = veh.conducteurs.all().values_list("email", flat=True)
            if usercurrent.email in idd:
                cpt = 'oui'
            else:
                cpt = 'non'

        if cpt == 'non':
            return Response({'message': "Engin ne faisant pas parti du parc de l'utilisateur !"},  status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if cpt == 'oui':
            if request.data['compt_act'] == "":
                return Response({'message': "Compteur incorrect, Veuillez renseigner le compteur"},  status=status.HTTP_406_NOT_ACCEPTABLE)
            
            else:
                client = get_tenant(request)
                with tenant_context(client):
                    datacopy =  request.data.copy()                               
                    last_enrg = Compteurs.objects.filter(vehicule_id=self.kwargs['engin_pk']).last()
                    
                    if last_enrg != None:
                        if Decimal(datacopy['compt_act']) >= Decimal(last_enrg.compt_act):
                            datacopy['last_compt'] = last_enrg.compt_act
                            datacopy['start_compt'] = last_enrg.start_compt
                            datacopy['ecart'] = Decimal(datacopy['compt_act']) - Decimal(last_enrg.start_compt)
                            datacopy['releveur'] = self.request.user.id

                            serializer = self.get_serializer(data=datacopy)
                            serializer.is_valid(raise_exception=True)                        
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        else:
                            return Response({'message': "Compteur incorrect, donnant un écart négatif avec le précédent"},  status=status.HTTP_406_NOT_ACCEPTABLE)
                
                    else:
                        datacopy['last_compt'] = datacopy['compt_act']
                        datacopy['start_compt'] = datacopy['compt_act']
                        datacopy['ecart'] = 0.0
                        datacopy['releveur'] = self.request.user.id

                        serializer = self.get_serializer(data=datacopy)
                        serializer.is_valid(raise_exception=True)                        
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)


class AlertEpViewSet(ListAPIView):
    serializer_class = AlerteEpSerializer
    def get_queryset(self): 
        list_operateur = ["UTIL", "OPER", "MAG"]
        list_chef = ["CFONCT", "CGAR", "CMR", "DMR", "MDATA", "DGEN"]
        if self.request.user.type in list_operateur:
            return AlerteEp.objects.filter(utilisateur=self.request.user)
        elif self.request.user.type in list_chef:
            return AlerteEp.objects.all()


class ListAlertEp(ListAPIView):
    serializer_class = AlerteEpSerializer

    def get_queryset(self): 
        my_user = self.request.user
        liste_gest = ["DIR_EXPLOIT", "MASTER_DATA" "DIR_GEN"]
        liste_oper = ["CHEF_SITE", "CHEF_CTECH" "CHEF_AGENCE", "CHEF_REGION", "DIR_OPER"]
        if my_user.type == "CHEF_SMRLT":        
            return AlerteEp.objects.filter(chef_smrlt=my_user)

        elif my_user.type in liste_oper:         
            return AlerteEp.objects.filter(destinataires__contains=my_user)

        elif my_user.type in liste_gest:
            return AlerteEp.objects.all()
            

class ListCountEpCritiq(ListAPIView):
    serializer_class = CountCritiqSerializer
    queryset = CountCritique.objects.all()


