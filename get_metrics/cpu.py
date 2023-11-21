def get_cpu(resource, svc_list):
    cpu = []
    for pod in resource["items"]:
        usage = pod['containers'][0]["usage"]["cpu"].replace('n','')
        if pod["metadata"]["labels"]["name"] in svc_list:
            if "m" in usage:
                usage = usage[:-1]
            
            usage = int(usage)

            cpu.append(usage)

    return cpu
