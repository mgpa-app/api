from django.shortcuts import render
from mgpa.middleware import get_tenant
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework import status
import pandas as pd
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import ValidationElement, Eses, NumPrefix, Organigramme, PieceRechange, Prestations
from .EntrepriseSerializer import ValidationSerializer, EseSerializer, NumPrefixSerializer, AbonnementSerializer, OrganigramSerializer, ImportOrgFonctSerializer, PrestationSerializer, PieceRechangeSerializer
from Client.models import AbonneClient, Clients
from Client.ClientSerializers import AbonneClientSerializer
import secrets
import string
from django_tenants.utils import tenant_context,schema_context
from django.db import transaction




class EseValidation(CreateAPIView):
    serializer_class = ValidationSerializer
    parser_classes =  [FormParser, MultiPartParser]

    

    def create(self, request, *args, **kwargs):        
        data = request.data
        code_ese = data["code_ese"]
        nom_ese = data["nom_ese"].lower()

        abonne = AbonneClient.objects.filter(code=code_ese, is_active=True).first()
        # schem = AbonneClient.objects.values_list("schema_name", flat=True).first()
        
        print("********************************************************\n")
        print(abonne)

        # try:
        # with transaction.atomic():
    
        if abonne != None:

            client = Clients.objects.filter(schema_name=abonne.schema_name).first()
            if client == None:
                return Response("Identifiants erronés, veuillez vous rassurez se l'exactitude de ces identifiants")
            else:
                with tenant_context(client):
                    if Eses.objects.all().exists() == False:

                        data_ese = {}
                        

                        # CREATION DU MODEL ENTREPRISE
                        client = abonne.ese
                        # with tenant_context(client):
                        data_ese['nom_ese'] = nom_ese
                        data_ese['adresse_ese'] = abonne.ese.adresse
                        data_ese['abrev_ese']   = abonne.ese.schema_sigle
                        data_ese["schema_name"] = abonne.ese.schema_name
                        data_ese["domaine_ese"] = abonne.ese.nom_domaine
                        data_ese["datecreat_ese"] = abonne.ese.created_on
                        data_ese['slogan_ese']  = abonne.ese.slogan
                        data_ese['siege_ese']   = abonne.ese.ville_siege
                        data_ese['pays_ese']    = abonne.ese.pays
                        data_ese['email_ese']   = abonne.ese.email
                        data_ese['siteweb_ese'] = abonne.ese.siteweb
                        data_ese['user_admin_ese'] = abonne.ese.user_admin
                        data_ese['mdp_admin_ese'] = abonne.ese.mdp_admin
                        data_ese['description_ese']  = abonne.ese.description_ese
                        data_ese['logo_ese']    = abonne.ese.logo_ese
                        data_ese['phone1_ese']  = abonne.ese.phone1
                        data_ese['phone2_ese']  = abonne.ese.phone2
                        data_ese['num_contrib_ese'] = abonne.ese.niu_ese     

                        serializer_valid = EseSerializer(data=data_ese)
                        serializer_valid.is_valid(raise_exception=True)
                        serializer_valid.save()

                        # CREATION DES NUMEROS DE DEMANDE DE TRAVAIL POUR EP

                        digits = string.digits
                        code_length = 3
                        nbre = 0
                        set_prefix = {'000'}
                        data = {}
                        while nbre < 10:
                            cod = ""   
                            for i in range(code_length):
                                cod += "".join(secrets.choice(digits))
                            set_prefix.add(cod)
                            nbre += 1
                        for prefix in set_prefix:
                            data['entete'] = "DTEP"
                            data['prefix'] = prefix
                        
                            serializer_prefix = NumPrefixSerializer(data=data)
                            serializer_prefix.is_valid(raise_exception=True)
                            serializer_prefix.save()
                        set_prefix.clear()
                        
                    # CREATION DES NUMEROS DE DEMANDE DE TRAVAIL POUR CURATIFS
                        
                        digit = string.digits
                        nbre = 0
                        set_prefix = {'000'}
                        data = {}
                        while nbre < 10:
                            cod = ""
                            for i in range(code_length):
                                cod += "".join(secrets.choice(digit))
                            set_prefix.add(cod)
                            nbre += 1
                        for prefix in set_prefix:
                            data['entete'] = "DTCUR"
                            data['prefix'] = prefix
                        
                            serializer_prefix = NumPrefixSerializer(data=data)
                            serializer_prefix.is_valid(raise_exception=True)
                            serializer_prefix.save()
                        set_prefix.clear()



                        serializers = AbonneClientSerializer(abonne)
                        serialized_data = serializers.data

                        reab = AbonneClient.objects.filter(code=code_ese).filter(is_active=True).first()

                            
                        data_ab = {}
                        data_ab['ese'] = reab.ese.id_enreg
                        
                        data_ab['date_saisie'] = reab.date_saisie
                        
                        data_ab['num_abon'] = reab.num_abon

                        data_ab['schema_name'] = reab.schema_name
                        
                        data_ab['date_debut'] = reab.date_debut
                        
                        data_ab['mensualite'] = reab.mensualite
                        
                        data_ab['date_fin'] = reab.date_fin
                        
                        data_ab['code'] = reab.code
                        data_ab['nbre_man'] = reab.nbre_man
                        data_ab['nbre_vl'] = reab.nbre_vl
                        
                        data_ab['nbre_pl1'] = reab.nbre_pl1
                        
                        data_ab['nbre_pl2'] = reab.nbre_pl2
                        
                        data_ab['nbre_autobus'] = reab.nbre_autobus
                        data_ab['nbre_gc'] = reab.nbre_gc
                        data_ab['prcent_remise'] = reab.prcent_remise
                        data_ab['nusers_dg'] = reab.nusers_dg
                        
                        data_ab['nusers_dop'] = reab.nusers_dop
                        data_ab['nusers_dex'] = reab.nusers_dex
                        data_ab['nusers_srm'] = reab.nusers_srm
                        data_ab['nusers_reg'] = reab.nusers_reg
                        data_ab['nusers_age'] = reab.nusers_age
                        data_ab['nusers_ctq'] = reab.nusers_ctq
                        data_ab['nusers_util'] = reab.nusers_util
                        data_ab['nusers_gar'] = reab.nusers_gar
                        data_ab['nusers_mag'] = reab.nusers_mag
                        data_ab['nbre_users'] = reab.nbre_users()
                        data_ab['nbre_engins'] = reab.nbre_engins()
                        data_ab['montant_engins'] = round(serialized_data["montant_engins"], 0)
                        data_ab['montant_users'] = round(serialized_data["montant_users"], 0)
                        data_ab['montant_ht'] = round(serialized_data["montant_ht"], 0)
                        # data_ab['montant_taxe'] = round(serialized_data["montant_taxe"], 0)
                        data_ab['montant_ttc'] = round(serialized_data["montant_ttc"], 0)
                        data_ab['montant_verse'] = reab.montant_verse
                        data_ab['montant_restant'] = round(serialized_data["montant_restant"], 0)
                        data_ab['date_next_versement'] = reab.date_next_versement
                        data_ab['is_active'] = reab.is_active

                        
                        serializ = AbonnementSerializer(data=data_ab)
                        serializ.is_valid(raise_exception=True)
                        serializ.save()
                        print(serializ)

                        User = get_user_model()
                        
                        User.objects.create_user(
                            email= abonne.ese.user_admin,
                            password=abonne.ese.mdp_admin,
                            username="Admin",
                            last_name="Admin",
                            first_name="",
                            matricule = '',
                            mobile = '',
                            type = 'MASTER_DATA',
                            poste = 'Administrateur',
                            site = Organigramme.objects.filter(organigramme="DG").first(),
                            date_nais = None,
                            genre = '',
                            matrimonial = '',
                            address = '',
                            avatar = None,
                            permis = '',
                            num_cni = '',
                            signature = None,       
            
                        )
                            
                        return Response(serializer_valid.data, status=status.HTTP_200_OK) 
                        




                    else:
                    
                        serializers = AbonneClientSerializer(abonne)
                        serialized_data = serializers.data

                        reab = AbonneClient.objects.filter(code=code_ese).filter(is_active=True).first()

                            
                        data_ab = {}
                        data_ab['ese'] = reab.ese.id_enreg
                        
                        data_ab['date_saisie'] = reab.date_saisie
                        
                        data_ab['num_abon'] = reab.num_abon

                        data_ab['schema_name'] = reab.schema_name
                        
                        data_ab['date_debut'] = reab.date_debut
                        
                        data_ab['mensualite'] = reab.mensualite
                        
                        data_ab['date_fin'] = reab.date_fin
                        
                        data_ab['code'] = reab.code
                        data_ab['nbre_man'] = reab.nbre_man
                        data_ab['nbre_vl'] = reab.nbre_vl
                        
                        data_ab['nbre_pl1'] = reab.nbre_pl1
                        
                        data_ab['nbre_pl2'] = reab.nbre_pl2
                        
                        data_ab['nbre_autobus'] = reab.nbre_autobus
                        data_ab['nbre_gc'] = reab.nbre_gc
                        data_ab['prcent_remise'] = reab.prcent_remise
                        data_ab['nusers_dg'] = reab.nusers_dg
                        
                        data_ab['nusers_dop'] = reab.nusers_dop
                        data_ab['nusers_dex'] = reab.nusers_dex
                        data_ab['nusers_srm'] = reab.nusers_srm
                        data_ab['nusers_reg'] = reab.nusers_reg
                        data_ab['nusers_age'] = reab.nusers_age
                        data_ab['nusers_ctq'] = reab.nusers_ctq
                        data_ab['nusers_util'] = reab.nusers_util
                        data_ab['nusers_gar'] = reab.nusers_gar
                        data_ab['nusers_mag'] = reab.nusers_mag
                        data_ab['nbre_users'] = reab.nbre_users()
                        data_ab['nbre_engins'] = reab.nbre_engins()
                        data_ab['montant_engins'] = round(serialized_data["montant_engins"], 0)
                        data_ab['montant_users'] = round(serialized_data["montant_users"], 0)
                        data_ab['montant_ht'] = round(serialized_data["montant_ht"], 0)
                        # data_ab['montant_taxe'] = round(serialized_data["montant_taxe"], 0)
                        data_ab['montant_ttc'] = round(serialized_data["montant_ttc"], 0)
                        data_ab['montant_verse'] = reab.montant_verse
                        data_ab['montant_restant'] = round(serialized_data["montant_restant"], 0)
                        data_ab['date_next_versement'] = reab.date_next_versement
                        data_ab['is_active'] = reab.is_active

                        
                        serializ = AbonnementSerializer(data=data_ab)
                        serializ.is_valid(raise_exception=True)
                        serializ.save()
                        print(serializ)
                            
                        return Response({'status': True, 'message': "abonnement validé"}, status=status.HTTP_200_OK)    
        else:
            return Response({'status': False, 'message':"Code ou nom de l'entreprise erroné! Veuillez renseigner convenablement le code et le nom de votre entreprise."}, status=status.HTTP_400_BAD_REQUEST)            

    # except Exception as e:
    #     return Response(str(e))  





class CreateOrganFonct(CreateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Organigramme.objects.all()
    serializer_class = OrganigramSerializer

    def post(self, request, *args, **kwargs):

        client = get_tenant(request)
        with tenant_context(client):

            data = request.data.copy()
            pos = ""
            pos += "".join(str(client.schema_name).strip().upper())
            pos += "".join("_")
            pos += "".join(str(data['direction_gen']).upper())

            if data['direction_fonct'] !="":
                pos += "".join("_")
                pos += "".join(str(data['direction_fonct']).upper())

            if data['service'] !="":
                pos += "".join("_")
                pos += "".join(str(data['service']).upper())

            if data['agence'] !="":
                pos += "".join("_")
                pos += "".join(str(data['agence']).upper())

            if data['site'] !="":
                pos += "".join("_")
                pos += "".join(str(data['site']).upper())

            data['organigramme'] = pos.upper()

            serializer = OrganigramSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ListOrganFonct(ListAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Organigramme.objects.all()
    serializer_class = OrganigramSerializer

class UpdateOrganFonct(RetrieveUpdateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Organigramme.objects.all()
    serializer_class = OrganigramSerializer



    def update(self, request, *args, **kwargs):
        client = get_tenant(request)
        with tenant_context(client):

            instance = Organigramme.objects.get(id=kwargs['pk'])

            data = request.data.copy()

            pos = ""
            pos += "".join(str(client.schema_name).strip().upper())
            pos += "".join("_")
            pos += "".join(str(data['direction_gen']).strip().upper())

            if data['direction_fonct'] !="":
                pos += "".join("_")
                pos += "".join(str(data['direction_fonct']).strip().upper())

            if data['service'] !="":
                pos += "".join("_")
                pos += "".join(str(data['service']).strip().upper())

            if data['agence'] !="":
                pos += "".join("_")
                pos += "".join(str(data['agence']).strip().upper())

            if data['site'] !="":
                pos += "".join("_")
                pos += "".join(str(data['site']).strip().upper())
            
            if data['sous_site'] !="":
                pos += "".join("_")
                pos += "".join(str(data['sous_site']).strip().upper())

            data['organigramme'] = pos.strip().upper()

            serializer = OrganigramSerializer(instance, data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

class DelOrganFonct(DestroyAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Organigramme.objects.all()
    serializer_class = OrganigramSerializer
    lookup_field = 'pk'


class ImportOrgFonctView(APIView):
    serializer_class = ImportOrgFonctSerializer
    parser_classes =  [FormParser, MultiPartParser]

    def post(self, request):
        cliente = get_tenant(request)

        data = request.FILES
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': 'Veuillez pourvoir un fichier valide'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        excel_file = data.get('file')
        df = pd.read_excel(excel_file, sheet_name=0)
        
        with tenant_context(cliente):
            
            for k in range(len(df)):

                pos = ""
                
                data_org = {}
                if str(df.iloc[k, 0]).strip() != "":
                    data_org['direction_gen'] = str(df.iloc[k, 0]).strip().upper()
                    pos += "".join(str(cliente.schema_name).strip().upper())
                    pos += "".join("_")
                    pos += "".join(str(df.iloc[k, 0]).strip().upper())
                    

                if str(df.iloc[k, 1]).strip() != "" :
                    if str(df.iloc[k, 1]).strip() != "nan":
                        data_org['direction_fonct'] = str(df.iloc[k, 1]).strip().upper()
                        if pos == "":
                            pos += "".join(str(df.iloc[k, 1]).strip()).upper()
                        else:
                            pos += "".join("_")
                            pos += "".join(str(df.iloc[k, 1]).strip()).upper()
                    
                
                if str(df.iloc[k, 2]).strip() != "":
                    if str(df.iloc[k, 2]).strip() != "nan":
                        data_org['service'] = str(df.iloc[k, 2]).strip().upper()
                        if pos == "":
                            pos += "".join(str(df.iloc[k, 2]).strip()).upper()
                        else:
                            pos += "".join("_")
                            pos += "".join(str(df.iloc[k, 2]).strip()).upper()
                        
                
                if str(df.iloc[k, 3]).strip() != "":
                    if str(df.iloc[k, 3]).strip() != "nan":
                        data_org['agence'] = str(df.iloc[k, 3]).strip().upper()
                        if pos == "":
                            pos += "".join(str(df.iloc[k, 3]).strip()).upper()
                        else:
                            pos += "".join("_")
                            pos += "".join(str(df.iloc[k, 3]).strip()).upper()
                    
                
                if str(df.iloc[k, 4]).strip() != "":
                    if str(df.iloc[k, 4]).strip() != "nan":
                        data_org['site'] = str(df.iloc[k, 4]).strip().upper()
                        if pos == "":
                            pos += "".join(str(df.iloc[k, 4]).strip()).upper()
                        else:
                            pos += "".join("_")
                            pos += "".join(str(df.iloc[k, 4]).strip()).upper()
                    
                
                if str(df.iloc[k, 5]).strip() != "":
                    if str(df.iloc[k, 5]).strip() != "nan":
                        data_org['sous_site'] = str(df.iloc[k, 5]).strip().upper()
                        if pos == "":
                            pos += "".join(str(df.iloc[k, 5]).strip()).upper()
                        else:
                            pos += "".join("_")
                            pos += "".join(str(df.iloc[k, 5]).strip()).upper()
                    
                
                
                data_org['organigramme'] = pos.upper()
                serializer_org = OrganigramSerializer(data=data_org)
                if serializer_org.is_valid(raise_exception=True):
                    serializer_org.save()
        
        return Response({
                'status': True,
                'message': "Fichier des organigammes importé avec succès.",
                
            }, status=status.HTTP_201_CREATED)


# CRUD POUR LES PRESTATIONS

class ListPrestations(ListAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Prestations.objects.all()
    serializer_class = PrestationSerializer


class CreatePrestations(CreateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Prestations.objects.all()
    serializer_class = PrestationSerializer


class UpdatePrestations(RetrieveUpdateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Prestations.objects.all()
    serializer_class = PrestationSerializer


class DeletePrestations(DestroyAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = Prestations.objects.all()
    serializer_class = PrestationSerializer



# CRUD POUR LES PIECES DE RECHANGE

class ListPieceRechange(ListAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = PieceRechange.objects.all()
    serializer_class = PieceRechangeSerializer


class CreatePieceRechange(CreateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = PieceRechange.objects.all()
    serializer_class = PieceRechangeSerializer


class UpdatePieceRechange(RetrieveUpdateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = PieceRechange.objects.all()
    serializer_class = PieceRechangeSerializer


class DeletePieceRechange(DestroyAPIView):
    parser_classes = [FormParser, MultiPartParser]
    queryset = PieceRechange.objects.all()
    serializer_class = PieceRechangeSerializer