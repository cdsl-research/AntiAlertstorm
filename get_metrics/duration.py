def get_duration(data, limit):
    name_duration = {}
    for i in range(limit):
        try:
            traceID = data['data'][i]
        except IndexError: 
            print(f"Number of traceID under limit")
            break

        for j in range(len(traceID['spans'])):
            operationName = traceID['spans'][j]['operationName']
            duration = traceID['spans'][j]['duration']
            if (operationName not in name_duration ):
                name_duration[operationName] = [duration]
                name_duration[operationName].append(1)
            else:
                name_duration[operationName][0] += duration
                name_duration[operationName][1] += 1
    ave = []
    for ope in name_duration.keys():
        ave.append(int(name_duration[ope][0] / name_duration[ope][1]))

    try:
        maxave = max(ave)
    except ValueError:
        maxave = 1

    return maxave