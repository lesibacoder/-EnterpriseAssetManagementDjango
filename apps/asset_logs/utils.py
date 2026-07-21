from .models import AssetLog


def create_asset_log(
    asset,
    action,
    user=None,
    description="",
):

    AssetLog.objects.create(
        asset=asset,
        action=action,
        user=user,
        description=description,
    )