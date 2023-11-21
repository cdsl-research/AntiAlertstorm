def pre(cpu, duration, limit):
    if cpu == 0:
        pre = 0
        return pre
    
    else:
        pre = (cpu / duration) * limit

    return pre

def rate(cpu, pre_cpu):
    try:
        rate = round(cpu / pre_cpu * 100, 1)
    except ZeroDivisionError:
        rate = 0
    return rate