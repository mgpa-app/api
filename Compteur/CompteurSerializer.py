from rest_framework import serializers
from django.conf import settings
from.models import Compteurs, AlerteEp, CptAlert, CountCritique
from Matroulant.models import VehiculesEses
from Matroulant.MatroulantSerializer import VehSerializer
from django.db.models import Q
from mgpa.middleware import get_tenant
from django_tenants.utils import tenant_context
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404



class CompteurCreateSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Compteurs
        fields = ["compt_act"]
            
    def create(self, validated_data):
        engin_id = self.context['engin_id'] 
        return Compteurs.objects.create(vehicule_id=engin_id, **validated_data)



class CompteurSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Compteurs
        fields = ["id", "start_compt", "last_compt", "compt_act", "date_compt", "ecart", "releveur", "statut_compt", "vehicule"]
            
    def create(self, validated_data):
        engin_id = self.context['engin_id'] 
        return Compteurs.objects.create(vehicule_id=engin_id, **validated_data)



class AlerteEpSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlerteEp
        fields = ["id", "destinataires", "alerte", "message", "compt", "vehicule", "statut", "session_alert", 'ecart', 'type_alert', 'date_alert', 'nbalert', 'chef_smrlt']
        read_only_fields =["utilisateur"]

 

class CptAlertSerializer(serializers.ModelSerializer):
    alertep = AlerteEpSerializer()
    class Meta:
        model = CptAlert
        fields = ["id", "nbalert", "ecart", "date_alert", "alertep"]



class CountCritiqSerializer(serializers.ModelSerializer):

    class Meta:
        model = CountCritique
        fields = ["id", "date_count", "vehicule", "n_depassement", "n_danger", "n_critique", "ecart", "statut", "type_ep", "session"]
