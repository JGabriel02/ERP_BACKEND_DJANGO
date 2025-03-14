from rest_framework.exceptions import AuthenticationFailed, APIException
from django.contrib.auth.hashers import check_password, make_password
from accounts.models import User
from companies.models import Enterprise, Employee

class Authentication:
    def singin(self, email=None, password=None):
        exception_auth = AuthenticationFailed('Email e/ou senha incorreto(s)')
        user_exists = User.objects.filter(email=email).exists()
        
        if not user_exists:
            raise exception_auth
        
        user = User.objects.filter(email=email).first()
        
        if not check_password(password, user.password):
            raise exception_auth
        
        return user
    
    def signup(self, name, email, password, type_account='owner', company_id=None):
        # Validações dos campos obrigatórios
        if not name or name == "":
            raise AuthenticationFailed('O nome não deve ser Null')
        if not email or email == "":
            raise AuthenticationFailed('O email não deve ser Null')
        if not password or password == "":
            raise AuthenticationFailed('O password não deve ser Null')
    
        # Validação específica para funcionários
        if type_account == 'employee' and not company_id:
            raise AuthenticationFailed('O Id da empresa não deve ser Null')
        
        # Verifica se o e-mail já está cadastrado
        if User.objects.filter(email=email).exists():
            raise AuthenticationFailed('Este email já foi cadastrado na plataforma')
        
        # Cria o usuário
        password_hashed = make_password(password)
        is_owner = type_account == 'owner'  # Define is_owner como True para donos, False para funcionários

        created_user = User.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner=is_owner
        )
        
        # Se for um dono, cria uma empresa associada
        if type_account == 'owner':
            created_enterprise = Enterprise.objects.create(
                name='Nome da empresa',  # Você pode personalizar o nome da empresa
                user_id=created_user.id
            )
            company_id = created_enterprise.id  # Atualiza o company_id para uso posterior
        
        # Se for um funcionário, associa à empresa
        if type_account == 'employee':
            Employee.objects.create(
                enterprise_id=company_id,
                user_id=created_user.id
            )
            
        return created_user