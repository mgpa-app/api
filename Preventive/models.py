from django.db import models
from Matroulant.models import VehiculesEses
from django.conf import settings
import uuid
from Entreprise.models import Organigramme
from django.contrib.auth import get_user_model
from Entreprise.models import Prestations, PieceRechange



User = get_user_model()


class SuiviEp(models.Model):

    """_summary_

    Returns:
        _vehicule_: _Véhicule ou engin du suivi EP_
        _statut_ep_: _Status du suivi d'EP: soit EP effectué, soit en attente ou alors en statut de demande_
        _dernier_ep_: _Le dernier EP effectué_
        _comptlast_ep_: _Compteur du dernier EP effectué_
        _datelast_ep_: _Date du dernier EP effectué_
        _compt_act_: _Compteur actuel_
        _compt_cible_: _Compteur cible pour le prochain EP_
        _ecart_: _Ecart avec le compteur cible_
        _type_alert_: _Type d'alerte_
        _prochain_ep_: _Le prochain EP à effectuer_
        _statut_dt_: _Statut de la DT _
        _site_matrlt_: _Site du chef de parc du véhicule_
        _session_alerte_: _Session de l'alerte EP générée_
        

    """

    STATUTEP = [
        ("EFFECTUE", "EFFECTUE"),
        ("EN ATTENTE", "EN ATTENTE"),
        ("EN DEMANDE", "EN DEMANDE"),
        
    ]


    vehicule = models.ForeignKey(VehiculesEses, null=True, on_delete=models.SET_NULL, related_name='vehicule_suiviep')
    statut_ep = models.CharField(max_length=50, null=True, blank=True, choices=STATUTEP)
    dernier_ep = models.CharField(max_length=50, null=True, blank=True)
    comptlast_ep = models.FloatField()
    datelast_ep = models.DateField(null=True, blank=True)
    compt_act = models.FloatField()
    compt_cible = models.FloatField()
    ecart = models.FloatField()
    type_alert = models.CharField(max_length=255, blank=True, null=True)
    prochain_ep = models.CharField(max_length=50, null=True, blank=True)
    statut_dt = models.CharField(max_length=100, blank=True, null=True)
    site_matrlt = models.ForeignKey(Organigramme, null=True, blank=True, on_delete=models.SET_NULL, related_name='suivi_site_matrlt')
    session_alerte = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} - {} - {}".format(self.vehicule.immat, self.prochain_ep, self.statut_ep)
    

# TABLEAU DES EP EFFECTUES
class Eps(models.Model):

    """_summary_

    Returns:
        _type_: _description_
    """

    ETATEP = [
        ("EFFECTUE", "EFFECTUE"),
        ("NON EFFECTUE", "NON EFFECTUE"),   
    ]

    vehicule = models.ForeignKey(VehiculesEses, null=True, on_delete=models.SET_NULL, related_name='vehicule_eps')
    statut_dt = models.CharField(max_length=100, blank=True, null=True)
    type_ep = models.CharField(max_length=255, blank=True, null=True)
    compt_alert = models.FloatField()
    date_recept = models.DateField(auto_now_add=True)
    date_ep = models.DateField(null=True)
    compt_ep = models.FloatField(null=True)
    etat_ep = models.CharField(max_length=20, choices=ETATEP, default="NON EFFECTUE")
    observation = models.TextField()
    garagiste = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='garagiste_eps')

    def __str__(self):
        return "{} - {} - {}".format(self.vehicule.immat, self.type_ep, self.etat_ep)
