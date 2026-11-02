from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from Entreprise.models import Organigramme
from Entreprise.models import AbonnementEse



class UserAccountManager(BaseUserManager):
    def _create_user(self, email, username, password, first_name, last_name, matricule, mobile, type, poste, site, date_nais, genre, matrimonial, address, avatar, permis, num_cni, signature, **extra_fields):
        if not email:
            raise ValueError("Vous devez fournir une adresse mail")
        if not password:
            raise ValueError('Vous devez fournir un mot de passe')

        if type == "UTILISATEUR":
            nbre_ab = AbonnementEse.objects.last().nusers_util
            use = GlobalUser.objects.filter(type="UTILISATEUR").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "UTILISATEUR" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'


        if type == "GARAGISTE":
            nbre_ab = AbonnementEse.objects.last().nusers_gar
            use = GlobalUser.objects.filter(type="GARAGISTE").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "GARAGISTE" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'
        
                    
        if type == "MAGASINIER":
            nbre_ab = AbonnementEse.objects.last().nusers_mag
            use = GlobalUser.objects.filter(type="MAGASINIER").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "MAGASINIER" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'
        

        if type == "CHEF_SITE":
            nbre_ab = AbonnementEse.objects.last().nusers_site
            use = GlobalUser.objects.filter(type="CHEF_SITE").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "CHEF_SITE" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'
        
                    
        if type == "CHEF_CTECH":
            nbre_ab = AbonnementEse.objects.last().nusers_ctq
            use = GlobalUser.objects.filter(type="CHEF_CTECH").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "CHEF_CTECH" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'


        if type == "CHEF_AGENCE":
            nbre_ab = AbonnementEse.objects.last().nusers_age
            use = GlobalUser.objects.filter(type="CHEF_AGENCE").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "CHEF_AGENCE" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'
        
                    
        if type == "CHEF_REGION":
            nbre_ab = AbonnementEse.objects.last().nusers_reg
            use = GlobalUser.objects.filter(type="CHEF_REGION").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "CHEF_REGION" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'


        if type == "CHEF_SMRLT":
            nbre_ab = AbonnementEse.objects.last().nusers_srm
            use = GlobalUser.objects.filter(type="CHEF_SMRLT").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "CHEF_SMRLT" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'


        if type == "DIR_EXPLOIT":
            nbre_ab = AbonnementEse.objects.last().nusers_dex
            use = GlobalUser.objects.filter(type="DIR_EXPLOIT").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "DIR_EXPLOIT" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'


        if type == "DIR_OPER":
            nbre_ab = AbonnementEse.objects.last().nusers_dop
            use = GlobalUser.objects.filter(type="DIR_OPER").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "DIR_OPER" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'
        

        if type == "MASTER_DATA":
            nbre_ab = AbonnementEse.objects.last().nusers_data
            use = GlobalUser.objects.filter(type="MASTER_DATA").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "MASTER_DATA" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'



        if type == "DIR_GEN":
            nbre_ab = AbonnementEse.objects.last().nusers_dg
            use = GlobalUser.objects.filter(type="DIR_GEN").exists()
            if use and use.count() >= nbre_ab:
                return 'Le nombre maximum d\'utilisateur de type "DIR_GEN" est atteint, vous ne pouvez plus créer ce type d\'utilisateur'



        UserAccount = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            matricule = matricule,
            mobile = mobile,
            type = type,
            poste = poste,
            site = site,
            date_nais = date_nais,
            genre = genre,
            matrimonial = matrimonial,
            address = address,
            avatar = avatar,
            permis = permis,
            num_cni = num_cni,
            signature = signature,
            
            **extra_fields
        )

        UserAccount.set_password(password)
        UserAccount.save(using=self._db)
        
        
        return UserAccount

    def create_user(self, email, username, password, first_name, last_name, matricule, mobile, type, poste, site, date_nais, genre, matrimonial, address, avatar, permis, num_cni, signature, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, username, password, first_name, last_name, matricule, mobile, type, poste, site, date_nais, genre, matrimonial, address, avatar, permis, num_cni, signature, **extra_fields)

    def create_superuser(self, email, username, password, first_name, last_name, matricule, mobile, type, poste, site, date_nais, genre, matrimonial, address, avatar, permis, num_cni, signature, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email, username, password, first_name, last_name, matricule, mobile, type, poste, site, date_nais, genre, matrimonial, address, avatar, permis, num_cni, signature, **extra_fields)



class GlobalUser(AbstractUser, PermissionsMixin):
    """_summary_

    Args:
        AbstractUser (_type_): _description_
        PermissionsMixin (_type_): _description_

    Returns:
        _type_: _description_
    """

    # USER_CATEGORIES = (
    #     ("super_admin", "super_admin"),
    #     ("public_platform", "public_platform"),
    #     ("client_staff", "client_staff"),
        
    # )

    users_types = {
        ("UTILISATEUR", "UTILISATEUR"),
        ("GARAGISTE", "GARAGISTE"),
        ("MAGASINIER", "MAGASINIER"),
        ("CHEF_SITE", "CHEF_SITE"),
        ("CHEF_CTECH", "CHEF_CTECH"),
        ("CHEF_AGENCE", "CHEF_AGENCE"),
        ("CHEF_REGION", "CHEF_REGION"),
        ("CHEF_SMRLT", "CHEF_SMRLT"),
        ("DIR_EXPLOIT", "DIR_EXPLOIT"),
        ("DIR_OPER", "DIR_OPER"),
        ("MASTER_DATA", "MASTER_DATA"),
        ("DIR_GEN", "DIR_GEN"),
    
    }
    
    GENRES = {
        ('MASCULIN', 'MASCULIN'),
        ('FEMININ', 'FEMININ'),
    }
    
    MATRIMONIAL = {
        ('MARIE', 'MARIE'),
        ('CELIBATAIRE', 'CELIBATAIRE'),
    }

    username = models.CharField(max_length=255, unique=True, blank=True)
    email = models.EmailField(max_length=255, null=False, unique=True, db_index=True)  
    first_name = models.CharField(max_length=255, null=True,blank=True)
    last_name = models.CharField(max_length=255, null=True,blank=True)
    # user_category = models.CharField(max_length=50, choices=USER_CATEGORIES, default="client_staff")
    matricule = models.CharField(max_length=255, null=True, blank=True) 
    mobile = models.CharField(max_length=255, null=True,blank=True)
    type = models.CharField(max_length=50, blank=True, choices=users_types, default="MASTER_DATA")
    poste = models.CharField(max_length=255, null=True,blank=True)
    site = models.ForeignKey(Organigramme, null=True, blank=True, on_delete=models.SET_NULL, related_name='site_user')
    date_nais = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=50, blank=True, choices=GENRES)
    matrimonial = models.CharField(max_length=50, blank=True, choices=MATRIMONIAL)
    address = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, default="user3.png")
    permis = models.CharField(max_length=255, null=True,blank=True)
    num_cni = models.CharField(max_length=255, null=True,blank=True)
    signature = models.ImageField(upload_to='signatures', null=True, blank=True)
    is_staff = models.BooleanField(default=True) # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True) # must needed, otherwise you won't be able to loginto django-admin.
    is_superuser = models.BooleanField(default=False) # this field we inherit from PermissionsMixin.

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'matricule', 'mobile', 'type', 'poste', 'site', 'date_nais', 'genre', 'matrimonial', 'address', 'avatar', 'permis', 'num_cni', 'signature']

    @property
    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def is_global_user(self):
        return self.user_category in ("public_platform", "super_admin")

    @property
    def is_tenant_user(self):
        return self.user_category.startswith("client_")

    

    # def save(self, *, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
    #     if self.user_category == "super_admin":
    #         self.is_staff = True
    #         self.is_superuser = True
    #     elif self.user_category == "public_platform":
    #         self.is_staff = True
    #         self.is_superuser = False
    #     else:
    #         self.is_staff = False
    #         self.is_superuser = False
    #     return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    