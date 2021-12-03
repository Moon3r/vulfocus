from rest_framework.decorators import api_view
from django.http import JsonResponse
from frp.models import FrpUtils, FrpConfig
from dockerapi.models import ContainerVul
from dockerapi.common import R


@api_view(http_method_names=["GET"])
def get_config(request):
    """
    获取frp基本配置
    :param request:
    :return:
    """
    user = request.user
    if not user.is_superuser:
        return JsonResponse(R.build(msg="权限不足"))
    config = get_setting_config()
    frp_all = get_all_frp()
    data = {
        "config": config,
        "all": frp_all
    }
    return JsonResponse(R.ok(data=data))


@api_view(http_method_names=["POST"])
def set_config(request):
    """
        更新frp基本配置
        :param request:
        :return:
        """
    user = request.user
    if not user.is_superuser:
        return JsonResponse(R.build(msg="权限不足"))

    domain = request.POST.get("domain")
    frp_template = request.POST.get("frp_template")
    switch = request.POST.get("switch")
    frp_url = request.POST.get("frp_url")
    domain_config = FrpConfig.objects.filter(frp_key="domain").first()
    if not domain_config:
        domain_config_set = FrpConfig(frp_key="domain", frp_value=domain)
        domain_config_set.save()
    else:
        if domain_config.frp_value != domain:
            domain_config.frp_value = domain
            domain_config.save()
    template_config = FrpConfig.objects.filter(frp_key="frp_template").first()
    if not template_config:
        template_config_set = FrpConfig(frp_key="frp_template", frp_value=frp_template)
        template_config_set.save()
    else:
        if template_config.frp_value != frp_template:
            template_config.frp_value = frp_template
            template_config.save()
    switch_config = FrpConfig.objects.filter(frp_key="switch").first()
    if not switch_config:
        switch_config_set = FrpConfig(frp_key="switch", frp_value=switch)
        switch_config_set.save()
    else:
        if switch_config.frp_value != switch:
            switch_config.frp_value = switch
            switch_config.save()
    frps_url = FrpConfig.objects.filter(frp_key="frp_url").first()
    if not frps_url:
        frp_url_set = FrpConfig(frp_key="frp_url", frp_value=frp_url)
        frp_url_set.save()
    else:
        if frps_url.frp_value != frp_url:
            frps_url.frp_value = frp_url
            frps_url.save()

    configs = get_setting_config()
    return JsonResponse(R.ok(msg="修改成功", data=configs))


@api_view(http_method_names=["POST"])
def delete_frp(request):
    user = request.user
    if not user.is_superuser:
        return JsonResponse(R.build(msg="权限不足"))

    frpid = request.POST.get("frpid")
    try:
        frpc = FrpUtils.objects.get(frp_id=frpid)
        frpc.delete()
        config = get_setting_config()
        frp_all = get_all_frp()
        data = {
            "config": config,
            "all": frp_all
        }
        return JsonResponse(R.ok(msg="删除成功", data=data))
    except:
        return JsonResponse(R.err(msg="服务器内部错误"))


def get_all_frp():
    frps = FrpUtils.objects.all()
    rsp_data = {}
    rdata = []
    try:
        for frp in frps:
            container = ContainerVul.objects.get(container_id=frp.container_id)
            rsp_data['frpid'] = frp.frp_id
            rsp_data['frp_subdomain'] = frp.subdomain
            rsp_data['frpconfig'] = frp.frp_config
            rsp_data['dockerid'] = container.docker_container_id
            rsp_data['container_status'] = container.container_status
            rsp_data['container_port'] = container.container_port
            rdata.append(rsp_data)
            rsp_data = {}
    except:
        pass

    return rdata


def get_setting_config():
    configs = FrpConfig.objects.all()
    rsp_data = {}
    for config in configs:
        if not config.frp_key == "switch":
            rsp_data[config.frp_key] = config.frp_value
        else:
            rsp_data[config.frp_key] = True if config.frp_value == "true" else False
    return rsp_data
