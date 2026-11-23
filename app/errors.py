"""Erreurs métier. Le contrôleur les traduit en codes HTTP."""


class InvalidRequest(Exception):
    """Données envoyées par le client invalides (service inconnu, numéro de téléphone incorrect...)."""


class ActiveTicketExists(Exception):
    """Le client a déjà un ticket en attente pour ce service dans ce bureau aujourd'hui."""
