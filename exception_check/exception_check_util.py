import util
import requests

pool_map = [
    {'ip': '192.168.3.165', 'port': '2131', 'domain': 'agent-web'},
    {'ip': '192.168.3.165', 'port': '2132', 'domain': 'back-finance-web'},
    {'ip': '192.168.3.165', 'port': '2134', 'domain': 'back-product-web'},
    {'ip': '192.168.3.165', 'port': '2136', 'domain': 'basics-promotion-service'},
    {'ip': '192.168.3.165', 'port': '2137', 'domain': 'cms-web'},
    {'ip': '192.168.3.165', 'port': '2138', 'domain': 'crm-web'},
    {'ip': '192.168.3.165', 'port': '2139', 'domain': 'frontier-trade-web'},
    # {'ip': '192.168.3.165', 'port': '2140', 'domain': 'horse-core'},
    # {'ip': '192.168.3.165', 'port': '2141', 'domain': 'index'},
    # {'ip': '192.168.3.165', 'port': '2142', 'domain': 'obi-web'},
    {'ip': '192.168.3.165', 'port': '2143', 'domain': 'odts-web'},
    # {'ip': '192.168.3.165', 'port': '2144', 'domain': 'ody-scheduler'},
    {'ip': '192.168.3.165', 'port': '2145', 'domain': 'oms-api'},
    {'ip': '192.168.3.165', 'port': '2146', 'domain': 'oms-dataex'},
    {'ip': '192.168.3.165', 'port': '2147', 'domain': 'oms-task'},
    {'ip': '192.168.3.165', 'port': '2148', 'domain': 'oms-web'},
    {'ip': '192.168.3.165', 'port': '2149', 'domain': 'opay-web'},
    {'ip': '192.168.3.165', 'port': '2150', 'domain': 'opms-web'},
    {'ip': '192.168.3.165', 'port': '2151', 'domain': 'ouser-web'},
    # {'ip': '192.168.3.165', 'port': '2152', 'domain': 'search'},
    {'ip': '192.168.3.165', 'port': '2153', 'domain': 'social-back-web'},
    {'ip': '192.168.3.165', 'port': '2154', 'domain': 'social-web'},
    {'ip': '192.168.3.165', 'port': '2156', 'domain': 'live-web'},
    {'ip': '192.168.3.165', 'port': '2133', 'domain': 'back-product-service'}
]

for i in pool_map:
    testBusinessException = util.HttpGet(
        'http://' + i['ip'] + ':' + i['port'] + '/' + i['domain'] + '/testException/testBusinessException')
    testBusinessException.execute()
    print(i['domain'])
    text = testBusinessException.get_text()
    print(' rest')
    if not text.__contains__('999999'):
        print('     ' + text)
    soa = util.HttpGet(
        'http://' + i['ip'] + ':' + i['port'] + '/' + i[
            'domain'] + '/cloud/pathInfo')
    soa.execute()
    if soa.get_text().startswith('['):
        testBusinessException = util.HttpGet(
            'http://' + i['ip'] + ':' + i['port'] + '/' + i[
                'domain'] + '/cloud/testExceptionService/testExceptionControllerAdvice')
        try:
            testBusinessException.execute()
        except requests.exceptions.ReadTimeout:
            print('     timeOut')
        text = testBusinessException.get_text()
        print(' soa')
        if not text.__contains__('999999'):
            print('     ' + text)
