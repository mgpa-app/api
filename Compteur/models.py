from django.db import models
from Matroulant.models import VehiculesEses
from django.contrib.auth import get_user_model
from django.conf import settings
import uuid
from Entreprise.models import Organigramme
from decimal import Decimal

User = get_user_model()

# TABLE DES COMPTEURS 
class Compteurs(models.Model):

    """_summary_

    Returns:
        _vehicule_: _Clé étrangère du modèle véhicule_
        _start_compt_: _Compteur de debut_
        _last_compt_: _Dernier compteur_
        _compt_act_: _Compteur actuel_
        _date_compt_: _Date de relevé du compteur_
        _releveur_: _Clé étrangère de l'utilisateur qui fait le relevé_
        _ecart_: _Ecart entre les derniers relevé et le compteur cible pour le prochain EP_
        _statut_compt_: _Statut du compteur. Soit usuels soit celui d'un EP_
    """

    STATUT_COMPT = [
        ("USUEL", "USUEL"),
        ("EP", "EP"),
        
    ]

    vehicule            = models.ForeignKey(VehiculesEses, null=True, on_delete= models.SET_NULL, related_name='veh_compteur')
    start_compt         = models.FloatField(null=True)
    last_compt          = models.FloatField(null=True)
    compt_act           = models.FloatField(null=True)
    date_compt          = models.DateTimeField(auto_now_add=True)
    releveur            = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,  on_delete=models.SET_NULL)
    ecart               = models.FloatField(null=True)
    statut_compt        = models.CharField(max_length=15, choices=STATUT_COMPT, default="USUEL")


    def __str__(self):
        return f"{self.vehicule.num_parc} - {self.compt_act} - {self.date_compt}"
    

class AlerteEp(models.Model):

    """_summary_

    Returns:
        _destinataires_: _Différents utilisateurs à signaler l'alerte de l'EP_
        _alerte_: _Prochain EP à effectuer _
        _message_: _Message d'alerte envoyé_
        _compt_: _Compteur à l'alerte_
        _type_alert_: _Type d'alete soit "A VIDANGER", soit "EN DEPASSEMENT" etc..._
        _date_alert_: _Date et heure de l'alerte_
        _ecart_: _Ecart commpteur au moment de l'alerte_
        _nbalert_: _Nombre d'alertes signalées pour la session_
        _vehicule_: _Véhicule concernée par l'alerte_
        _statut_: _Statut par rapport à l'EP programmé en instance_
        _chef_smrlt_: _ID du responsable du parc concerné par le véhicule_
        _session_alert_: _Session de l'alerte qui s'achève à l'exécution de l'EP programmé_
    """
    
    ALTEP = [
        ("0", "0"),
        ("250 H", "250 H"),
        ("500 H", "500 H"),
        ("750 H", "750 H"),
        ("1000 H", "1000 H"),
        ("1250 H", "1250 H"),
        ("1500 H", "1500 H"),
        ("1750 H", "1750 H"),
        ("2000 H", "2000 H"),
        ("5000 KM", "5000 KM"),
        ("10000 KM", "10000 KM"),
        ("15000 KM", "15000 KM"),
        ("20000 KM", "20000 H"),
        ("25000 KM", "25000 KM"),
        ("30000 KM", "30000 KM"),
        ("40000 KM", "40000 KM"),
        ("50000 KM", "50000 KM"),
        ("60000 KM", "60000 KM"),
        ("150 H", "150 H"),
        ("300 H", "300 H"),
        ("450 H", "450 H"),
        ("600 H", "600 H"),
        ("750 H", "750 H"),
        ("900 H", "900 H"),
        ("1050 H", "1050 H"),
        ("1200 H", "1200 H"),
        
    ]

    STATUT_ALERTE = [
        ("EN ATTENTE", "EN ATTENTE"),
        ("EN DEMANDE", "EN DEMANDE"),
        ("EFFECTUEE", "EFFECTUEE")
    ]

    TYPEALERT = [
        ("A VIDANGER", "A VIDANGER"),
        ("EN DEPASSEMENT", "EN DEPASSEMENT"),
        ("EN DEPASSEMENT DANGER", "EN DEPASSEMENT DANGER"),
        ("EN DEPASSEMENT CRITIQUE", "EN DEPASSEMENT CRITIQUE"),
    ]

    destinataires = models.ManyToManyField(User, blank=True, related_name="alertep_utilisateur")
    alerte = models.CharField("Alerte", max_length=50, blank=True, choices=ALTEP, default="0")
    message = models.CharField("Message", max_length=255, null=True, blank=True) 
    compt = models.FloatField()
    type_alert = models.CharField(max_length=50, blank=True, choices=TYPEALERT, default="A VIDANGER")
    date_alert = models.DateTimeField(auto_now_add=True)
    ecart = models.FloatField(blank=True, null=True, default=0.0)
    nbalert = models.PositiveIntegerField(default=0)
    vehicule = models.ForeignKey(VehiculesEses, null=True,  on_delete=models.SET_NULL)
    statut = models.CharField(max_length=50, blank=True, choices=STATUT_ALERTE, default="EN ATTENTE")    
    chef_smrlt = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_matrlt')
    session_alert = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return "Alerte {} -- vehicule : {}".format(self.alerte, self.vehicule.num_parc)
    


# LE NOMBRE DE MESSAGES ENVOYES PAR ALERTES D'EP

class CptAlert(models.Model):

    """_summary_

    Returns:
        _nbalert_: _Nombre d'aletes envoyées lors de la session_
        _ecart_: _Ecart avec le prochain EP programmé_
        _date_alert_: _Date et heure de l'alerte envoyée_
        _alertep_: _ID de l'alerte envoyée_
    """

    nbalert = models.PositiveIntegerField()
    ecart = models.FloatField()
    date_alert = models.DateTimeField(auto_now_add=True)
    alertep = models.ForeignKey(AlerteEp, on_delete=models.SET_NULL, blank=True, null=True, related_name='alert_cpt')

    def __str__(self):
        return "Alerte pour {}: {} fois".format(self.alertep.alerte, self.nbalert)


# TABLE DES COMPTES DES DEPASSEMENTS EFFECTUES PAR ALERTE EP
class CountCritique(models.Model):

    """_summary_

    Returns:
        _date_count_: _Date et heure du comptage_
        _vehicule_: _Véhicule de l'alerte_
        _n_depassement_: _Nombre d'alertes envoyées pour "Dépassement"_
        _n_danger_: _Nombre d'alertes envoyées pour "Danger"_
        _n_critique_: _Nombre d'alertes envoyées pour "Critique"_
        _ecart_: _Ecart lors de l'alerte_
        _session_: _Session de l'alerte_
        _statut_: _Statut de l'alerte, soit en instance soit déjà cloturée par l'exécution de EP_
        
    """

    OPTION = [
        ("OUVERT", "OUVERT"),
        ("FERME", "FERME"),
    ]

    date_count = models.DateTimeField(auto_now_add=True)
    vehicule = models.ForeignKey(VehiculesEses, null=True, on_delete=models.SET_NULL, related_name="veh_critique")
    n_depassement = models.PositiveIntegerField() 
    n_danger = models.PositiveIntegerField()
    n_critique = models.PositiveIntegerField()
    ecart = models.FloatField()
    type_ep = models.CharField(max_length=20, blank=True, null=True)
    session = models.CharField(max_length=100, blank=True, null=True)
    statut = models.CharField(max_length=25, choices=OPTION, default="OUVERT")

    def __str__(self):
        return "{}: Dépassement {} fois, Danger {} fois, Critique {} fois, session: {}".format(self.vehicule.immat, self.n_depassement, 
            self.n_danger, self.n_critique, self.session)