from wander_core.permissions import PermissionType, get_or_create_permission, ContentType, Permission


def add_user_permissions(user, model, name='', field_or_id=None,
                         permission_type: PermissionType = PermissionType.view):
    """
    give user some permission
    NOTICE: django有权限缓存策略，权限的临时更改需要再重新获取用户
    user = get_object_or_404(User, pk=user_id)
    """
    permission = get_or_create_permission(model=model, field_or_id=field_or_id,
                                          name=name,
                                          permission_type=permission_type)

    user.user_permissions.add(permission)


def remove_user_permissions(user, model, name='', field_or_id=None,
                            permission_type: PermissionType = PermissionType.view):
    """
    remove user permission
    """
    permission = get_or_create_permission(model=model, field_or_id=field_or_id,
                                          name=name,
                                          permission_type=permission_type)

    user.user_permissions.remove(permission)


def add_user_basic_model_permissions(user, model,
                                     permission_type: PermissionType):
    """
    给某个用户增加某个权限
    NOTICE: django有权限缓存策略，权限的临时更改需要再重新获取用户
    user = get_object_or_404(User, pk=user_id)
    """
    content_type = ContentType.objects.get_for_model(model)

    codename = f'{permission_type.value}_{content_type.model}'

    permission = Permission.objects.get(content_type=content_type,
                                        codename=codename)

    user.user_permissions.add(permission)


def remove_user_basic_model_permissions(user, model,
                                        permission_type: PermissionType):
    """
    给某个用户移除某个权限
    NOTICE: django有权限缓存策略，权限的临时更改需要再重新获取用户
    user = get_object_or_404(User, pk=user_id)
    """
    content_type = ContentType.objects.get_for_model(model)

    codename = f'{permission_type.value}_{content_type.model}'

    permission = Permission.objects.get(content_type=content_type,
                                        codename=codename)

    user.user_permissions.remove(permission)
