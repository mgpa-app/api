from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework import status
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from mgpa.middleware import get_tenant
from rest_framework.parsers import MultiPartParser, FormParser
from .PreventiveSerializer import SuiviEpSerializer
from .models import SuiviEp
from Entreprise.models import Organigramme
from guardian.shortcuts import get_objects_for_user


class ListSuiviEp(ListAPIView):
    serializer_class = SuiviEpSerializer
    parser_classes = [FormParser, MultiPartParser]
    # queryset = SuiviEp.objects.all()

    def get_queryset(self):
        # list_perms = ['PreventApps.view_suiviep']
        # return get_objects_for_user(self.request.user, list_perms)

    
        # # suivi = get_objects_for_user(self.request.user, 'PreventApps.view_suiviep')
        # # return suivi
        my_user = self.request.user
        liste_gest = ["DIR_EXPLOIT", "MASTER_DATA" "DIR_GEN"]
        liste_oper = ["CHEF_SITE", "CHEF_CTECH" "CHEF_AGENCE", "CHEF_REGION", "DIR_OPER"]
        
        if my_user.type == "CHEF_SMRLT":  
            return SuiviEp.objects.filter(site_matrlt_id=my_user.site_id)

        elif my_user.type in liste_oper:       
            return SuiviEp.objects.filter(vehicule__affectation__contains=my_user.site)

        elif my_user.type in liste_gest:
            return SuiviEp.objects.all()
