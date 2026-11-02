from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from Entreprise.EntrepriseSerializer import OrganigramSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    site = OrganigramSerializer()
    class Meta(BaseUserCreateSerializer.Meta):
        
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'matricule', 'mobile', 'type', 'poste', 'site', 'date_nais', 'genre', 'matrimonial', 'address', 'avatar', 'permis', 'num_cni', 'signature']

