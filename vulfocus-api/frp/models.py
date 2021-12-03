from django.db import models
import uuid


class FrpUtils(models.Model):
    """
    FrpUtils Model
    """
    frp_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    container_id = models.CharField(max_length=32, verbose_name='Docker容器运行ID')
    subdomain = models.CharField(max_length=255, verbose_name='访问子域名')
    frp_config = models.TextField(verbose_name='Frp代理配置', default='')

    class Meta:
        db_table = 'frp_utils'


class FrpConfig(models.Model):
    """
    FrpConfig Model
    """
    id = models.IntegerField(verbose_name="ID", primary_key=True)
    frp_key = models.CharField(max_length=255, verbose_name='配置名称', unique=True)
    frp_value = models.TextField(verbose_name='配置值', null=True, default='')

    class Meta:
        db_table = 'frp_config'
