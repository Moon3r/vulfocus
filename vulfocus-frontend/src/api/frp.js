import request from '@/utils/request'

/**
 * 获取frp配置
 * @param
 * @constructor
 */
export function frpSettings() {
    return request({
        url: '/frp/get',
        method: 'get'
    })
}


/**
 * 修改frp配置
 * @param data
 * @constructor
 */
export function settingUpdate(data) {
    return request({
        url: '/frp/update',
        method: 'post',
        data
    })
}


export function deleteFrpc(data) {
    return request({
        url: '/frp/delete',
        method: 'post',
        data
    })
}