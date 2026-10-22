from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from Client.models import Clients, Domain, AbonneClient
from django.template.loader import render_to_string


@receiver(post_save, sender=Clients)
def CreateTenant(sender, instance, created, **kwargs):
    if not created:
        dom = Domain.objects.filter(tenant_id = instance.id_enreg).first()
        dom.domain = instance.nom_domaine + ".localhost"   
        dom.save()

    else: 
        domain = Domain()
        domaine =  instance.nom_domaine + ".localhost"   # LE SOUS DOMAINE DE L'ENTREPRISE #
        domain.domain = domaine
        domain.tenant = instance     # domain.tenant = client
        domain.is_primary = True
        domain.save()


    # context={
    #     'nom_ese': instance.nom_ese,
    #     'adresse_ese': instance.adresse,
    #     'abrev_ese'  : instance.schema_sigle,
    #     "schema_name": instance.schema_name,
    #     "domaine_ese": instance.nom_domaine,
    #     'slogan_ese' : instance.slogan,
    #     'date_enreg': instance.created_on,
    #     'siege_ese'  : instance.ville_siege,
    #     'pays_ese'   : instance.pays,
    #     'email_ese'  : instance.email,
    #     'siteweb_ese': instance.siteweb,
    #     'user_admin_ese': instance.user_admin,
    #     'mdp_admin_ese': instance.mdp_admin,
    #     'description_ese' : instance.description_ese,
    #     'logo_ese'   : instance.logo_ese,
    #     'phone1_ese' : instance.phone1,
    #     'phone2_ese' : instance.phone2,
    #     'num_contrib_ese': instance.niu_ese,
         
    # }

    # try:
    #     text_html = render_to_string("Client/creationEse.html", context)
    #     msg = EmailMessage(
    #     "INSCRIPTION D'ENTREPRISE",
    #     text_html,
    #     "SORETAC <duparce.netzone@gmail.com>",
    #     [instance.email]
    #     )
    #     msg.content_subtype = "html"
    #     msg.send()

    # except Exception as e:
    #     print("Erreur de connexion internet")
