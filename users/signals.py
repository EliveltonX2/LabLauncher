# users/signals.py
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    """
    Este sinal é acionado logo após um novo usuário se cadastrar.
    Vamos definir a conta dele como inativa, pendente de aprovação
    do nosso CustomUser.is_approved.
    """
    user.is_active = False # Impede o login até que a conta seja ativada.
    # O campo 'is_approved' já é False por padrão no nosso modelo.
    user.save()
    print(f"Usuário {user.username} cadastrado e desativado, aguardando aprovação.")