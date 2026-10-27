from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
import uuid
import datetime
from django.core import validators

class Clients(TenantMixin):
    """INFORMATION DE L'ENTREPRISE CREEE

    Args:
        TenantMixin (_type_): _description_

    Returns:
        _type_: _description_
    """

    id_enreg            = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    schema_name         = models.CharField(max_length=255, unique=True)                         # Nom de location de l'entreprise dans la BD                                 
    created_on          = models.DateField("Date Enregistrement", auto_now_add=True)                                     # Date de creation de la location de l'entreprise
    nom_ese             = models.CharField("Nom Entreprise", max_length=255, blank=False, unique=True)
    schema_sigle        = models.CharField("Sigle Entreprise", max_length=255, unique=True)
    nom_domaine         = models.CharField("Nom Domaine Entreprise", max_length=255, default='localhost', unique=True)
    code_ab             = models.CharField(max_length=8)
    description_ese     = models.TextField("Description Entreprise", null=True, blank=True, default="Faire une description")
    email               = models.EmailField("Email Entreprise", max_length=255, unique=True, validators=[validators.EmailValidator(message="Email invalide")])
    siteweb             = models.CharField("Site web Entreprise", max_length=255, blank=True, null=True)
    slogan              = models.CharField("Slogan Entreprise", max_length=255, blank=True, null=True) 
    user_admin          = models.EmailField("Username admin", max_length=100, blank=True, null=True,  validators=[validators.EmailValidator(message="Email invalide")],)
    mdp_admin           = models.CharField("Mot de Passe Admin", max_length=255)  
    adresse             = models.CharField("Adresse Entreprise", max_length=255, blank=True, null=True)
    niu_ese             = models.CharField("NIU Entreprise", max_length=255, blank=True, null=True)
    ville_siege         = models.CharField("Ville Siège", max_length=255, blank=True, null=True)
    pays                = models.CharField("Pays Entreprise", max_length=255, blank=True, null=True)
    phone1              = models.CharField("N° Telephone 1", blank=True, null=True)
    phone2              = models.CharField ("N° Telephone 2", blank=True, null=True)
    logo_ese            = models.ImageField("Logo Entreprise", upload_to='logos', null=True, blank=True, default="logo.jpeg")
    ese_activate        = models.BooleanField("Activation Entreprise", default=False)
    auto_create_schema  = True
    auto_drop_schema    = True


    def save(self,*args, **kwargs):
        self.nom_ese = self.nom_ese.lower()
        self.schema_sigle = self.schema_sigle.lower()
        self.nom_domaine = self.nom_domaine.lower()
        self.email = self.email.lower()
        self.siteweb = self.siteweb.lower()
        return super(Clients, self).save(*args, **kwargs)

    class Meta: 
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return "{} ({}) - {}".format(self.nom_ese, self.schema_sigle, self.ese_activate)



class Domain(DomainMixin):
    pass




class Montants_Abonnements(models.Model):

    """MONTANT D'ABONNEMENT DES DIFFERENTS ENGINS ET TYPE D'UTILISATEUR

    Returns:
    mont_umag: montant de l'utilisateur type magasinier
    mont_ugar: montant de l'utilisateur type Chef garagiste
    mont_uutil: montant de l'utilisateur type chauffeur engin
    mont_uage: montant de l'utilisateur type chef d'agence
    mont_ureg: montant de l'utilisateur type chef de région
    mont_usrm: montant de l'utilisateur type chef du parc
    mont_udex: montant de l'utilisateur type directeur de département
    mont_udop: montant de l'utilisateur type directeur des parcs
    mont_udg: montant de l'utilisateur type directeur général

    """

    pourcent_taxe        = models.FloatField("Pourcentage Taxe", default=19.75)
    mont_vl              = models.PositiveIntegerField("Montant Véhicule Léger", default=0)
    mont_pl1             = models.PositiveIntegerField("Montant Poids Lourd 1", default=0)
    mont_pl2             = models.PositiveIntegerField("Montant Poids Lourd 2",default=0)
    mont_man             = models.PositiveIntegerField("Montant Engin Manutention",default=0) 
    mont_autobus         = models.PositiveIntegerField("Montant Autobus", default=0)
    mont_gc              = models.PositiveIntegerField("Montant Engin génie Civil", default=0) 
    mont_udg             = models.PositiveIntegerField("Montant Directeur Général", default=0) 
    mont_udop            = models.PositiveIntegerField("Montant Directeur Département", default=0) 
    mont_udex            = models.PositiveIntegerField("Montant Directeur des Parcs", default=0)
    mont_usrm            = models.PositiveIntegerField("Montant Chef de parc", default=0) 
    mont_ureg            = models.PositiveIntegerField("Montant Chef Région", default=0) 
    mont_uage            = models.PositiveIntegerField("Montant Chef Agence", default=0) 
    mont_uctq            = models.PositiveIntegerField("Montant Chef Technique", default=0) 
    mont_uutil           = models.PositiveIntegerField("Montant Chauffeur", default=0) 
    mont_ugar            = models.PositiveIntegerField("Montant Chef Garagiste", default=0)
    mont_umag            = models.PositiveIntegerField("Montant Magasinier", default=0)





class AbonneClient(models.Model):
    ese                         = models.ForeignKey(Clients, on_delete=models.SET_NULL, null=True, related_name="ese_abonne")
    num_abon                    = models.CharField(max_length=15)
    code                        = models.CharField("Code Entreprise", max_length=128, unique=True, blank=True, null=True)
    schema_name                 = models.CharField(max_length=255, unique=True, default="rien")     
    date_saisie                 = models.DateField(auto_now_add=True)
    date_debut                  = models.DateField()
    mensualite                  = models.PositiveIntegerField()
    date_fin                    = models.DateField()
    nbre_man                    = models.PositiveIntegerField("Nbre manutention", default=0)
    nbre_vl                     = models.PositiveIntegerField("Nbre Véhicule Léger", default=0)
    nbre_pl1                    = models.PositiveIntegerField("Nbre Poids Lourd 1", default=0)
    nbre_pl2                    = models.PositiveIntegerField("Nbre Poids Lourd 2", default=0)
    nbre_autobus                = models.PositiveIntegerField("Nbre Autobus", default=0)
    nbre_gc                     = models.PositiveIntegerField("Nbre Engin Génie civil", default=0)
    prcent_remise               = models.FloatField()
    nusers_dg                   = models.PositiveIntegerField("Direction Générale", default=0)
    nusers_dop                  = models.PositiveIntegerField("Département Opérations", default=0)
    nusers_dex                  = models.PositiveIntegerField("Département Exploitation", default=0)
    nusers_srm                  = models.PositiveIntegerField("Service Maintenance", default=0)
    nusers_reg                  = models.PositiveIntegerField("Région", default=0)
    nusers_age                  = models.PositiveIntegerField("Agence", default=0)
    nusers_ctq                  = models.PositiveIntegerField("Centre Technique", default=0)
    nusers_util                 = models.PositiveIntegerField("Utilisateur", default=0)
    nusers_gar                  = models.PositiveIntegerField("Garage", default=0)
    nusers_mag                  = models.PositiveIntegerField("Magasinier", default=0)  
    montant_verse               = models.PositiveIntegerField()
    date_next_versement         = models.DateField()
    is_active                   = models.BooleanField(default=True)

    def is_valid(self):
        return self.is_active and self.date_fin > datetime.date.today()

    def nbre_users(self):
        return int(self.nusers_dg) + int(self.nusers_dop) + int(self.nusers_dex) + int(self.nusers_srm) + int(self.nusers_reg) + int(self.nusers_age) + int(self.nusers_ctq) + int(self.nusers_util) + int(self.nusers_gar) + int(self.nusers_mag)

    def nbre_engins(self):
        return int(self.nbre_man) + int(self.nbre_vl) + int(self.nbre_pl1) + int(self.nbre_pl2) + int(self.nbre_autobus) + int(self.nbre_gc)


    def __str__(self):
        return "{} : du {} au {} ".format(self.ese.schema_sigle, self.date_debut, self.date_fin)