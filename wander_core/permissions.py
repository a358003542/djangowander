#!/usr/bin/env python
# -*-coding:utf-8-*-

from enum import Enum

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class PermissionType(Enum):
    view = 'view'
    add = 'add'
    change = 'change'
    delete = 'delete'


PermissionTypeDict = {
    'view': PermissionType.view,
    'add': PermissionType.add,
    'change': PermissionType.change,
    'delete': PermissionType.delete,
}


def get_permission_codename(model, field_or_id=None,
                            permission_type: PermissionType = PermissionType.view):
    """
    application permission codename:

    <type>_<content_type.mode>_<field_or_id>

    view_workflow_task

    view_form_field
    """
    content_type = ContentType.objects.get_for_model(model)

    if field_or_id:
        codename = f'{permission_type.value}_{content_type.model}_{field_or_id}'
    else:
        codename = f'{permission_type.value}_{content_type.model}'

    return codename


def get_or_create_permission(model, field_or_id=None, name='',
                             permission_type: PermissionType = PermissionType.view):
    if isinstance(model, str):
        from django.apps import apps
        res = model.split('.')
        if len(res) != 2:
            raise Exception('model structure is app_label.model_name')
        model = apps.get_model(app_label=res[0], model_name=res[1])

    codename = get_permission_codename(model, field_or_id=field_or_id,
                                       permission_type=permission_type)

    content_type = ContentType.objects.get_for_model(model)
    name = name if name else codename

    permission, _ = Permission.objects.get_or_create(
        codename=codename,
        content_type=content_type,
        defaults={'name': name}
    )

    return permission

