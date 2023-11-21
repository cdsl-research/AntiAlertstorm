from datetime import datetime
from kubernetes import client, config
from get_metrics import cpu, duration, csv
from alert import mail, verdict
import requests
import os
import time

def main(time, rate_svc):
    # get current time
    now = datetime.now()

    # interval ms
    interval = 3600000

    # duration limit μs
    duration_lim = 3000000

    # now(end)～$interval μs ago(start)
    ts_end = str(datetime.timestamp(now)).replace('.', '')
    ts_start = str(datetime.timestamp(now) - interval).replace('.', '')

    # serch limit
    limit = 20

    # get kubernetes svc
    svc_list = ['carts', 'catalogue', 'front-end', 'orders', 'user']
    namespace = "sock-shop"
    config.load_kube_config()
    api = client.CustomObjectsApi()
    v1 = client.CoreV1Api()
    resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="sock-shop", plural="pods")

    # get duration
    d_list = []
    for svc in svc_list: 
        # jaeger ui url
        URL = ( "http://localhost:16686/jaeger/api/traces?end="
                + ts_end 
                + "&limit=" + str(limit)
                + "&lookback=1h&maxDuration&minDuration"
                + "&service=" + svc + "." + namespace
                + "&start="+ ts_start )

        # get jaeger jason
        r = requests.get(URL)
        data = r.json()
        d_list.append(duration.get_duration(data, limit))

    # get cpu usage
    c = cpu.get_cpu(resource, svc_list)

    csvdata = []
    for i in range(len(svc_list)):
        pre_cpu = verdict.pre(c[i], d_list[i], duration_lim)
        rate_cpu = verdict.rate(c[i], pre_cpu)
        rate_svc[svc_list[i]] += rate_cpu
        predata = [svc_list[i], c[i], pre_cpu, rate_cpu]
        csvdata += [predata]

    # send alert
    if (time != 0) and (time % 60) == 0:
        for key in rate_svc.keys():
            rate_svc[key] /= 60
            if (100 >= rate_svc[key]) and (60 <= rate_svc[key]):
                mail.alert(key)
                print("mail")
            rate_svc[key] = 0

    return csvdata

if __name__ == "__main__":
    Time = 0
    rate_svc = {'carts': 0, 'catalogue': 0 , 'front-end': 0, 'orders': 0, 'user': 0}
    main(Time, rate_svc)
    header = ['svc', 'cpuusage', 'pre', 'rate']
    data = [header]

    while Time <= 300:
        data += main(Time, rate_svc)
        Time += 1
        time.sleep(1)

    path = ""
    csv.generate_csv(data, path, "")