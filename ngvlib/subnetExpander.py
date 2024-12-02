def subnetExpander(start, end):
    start = start.split(".")
    part3 = int(start[3])

    end = end.split(".")
    part6 = int(end[3])
    # print(parts[3])

    data = []
    for x in range(part3, part6 + 1):
        ips = (f"{start[0]}.{start[1]}.{start[2]}.{x}")
        data.append(ips)
        # print(part3 + 1)
    return data