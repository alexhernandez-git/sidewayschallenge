
# Django

# DRF

# Models

# Serializers

# Utilities
import environ
env = environ.Env()


def update_developer(dev, updated_dev):
    """Update the developer"""
    has_changed = False
    if dev.name != updated_dev['name']:
        dev.name = updated_dev['name']
        has_changed = True
    elif dev.username != updated_dev['username']:
        dev.username = updated_dev['username']
        has_changed = True
    elif has_changed:
        dev.save()


def update_organization(org, updated_org):
    """Update the orgeloper"""
    has_changed = False
    if org.login != updated_org['login']:
        org.login = updated_org['login']
        has_changed = True
    elif org.node_id != updated_org['node_id']:
        org.node_id = updated_org['node.id']
        has_changed = True
    elif org.url != updated_org['url']:
        org.url = updated_org['url']
    elif org.repos_url != updated_org['repos_url']:
        org.repos_url = updated_org['repos_url']
        has_changed = True
    elif org.events_url != updated_org['events_url']:
        org.events_url = updated_org['events_url']
        has_changed = True
    elif org.hooks_url != updated_org['hooks_url']:
        org.hooks_url = updated_org['hooks_url']
        has_changed = True
    elif org.issues_url != updated_org['issues_url']:
        org.issues_url = updated_org['issues_url']
        has_changed = True
    elif org.members_url != updated_org['members_url']:
        org.members_url = updated_org['members_url']
        has_changed = True
    elif org.public_members_url != updated_org['public_members_url']:
        org.public_members_url = updated_org['public_members_url']
        has_changed = True
    elif org.avatar_url != updated_org['avatar_url']:
        org.avatar_url = updated_org['avatar_url']
        has_changed = True
    elif org.description != updated_org['description']:
        org.description = updated_org['description']
        has_changed = True
    elif has_changed:
        org.save()
