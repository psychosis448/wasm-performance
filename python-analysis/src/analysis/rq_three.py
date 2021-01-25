from numpy import std, mean, median
from pandas import DataFrame
from statistics import geometric_mean
import matplotlib.pyplot as plt

def get_durations(benchmark):
    return list(map(lambda x : x['duration'], benchmark))

def calc_mean(benchmark):
    durations = get_durations(benchmark)
    return mean(durations)

def rq_three(mongo, device, log):
    data = list(mongo.db[device].find({
        "$or": [
            { "ua.browser.name" : { "$eq": "Firefox"}},
            { "ua.browser.name" : { "$eq": "Chrome"}},
            { "ua.browser.name" : { "$eq": "Safari"}},
            { "ua.browser.name" : { "$eq": "Mobile Safari"}},
            { "ua.browser.name" : { "$eq": "Samsung Browser"}},
        ]
    }))

    time_series_arr(data, device, "quicksort_int32array", log)
    time_series_arr(data, device, "fmr", log)
    time_series_arr(data, device, "bst_create", log)
    time_series_graph(data, device, "graph_create", log)
    time_series_graph(data, device, "graph_solve", log)

def time_series_arr(data, device, bench, log):
    result = []

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        for k, b in benchmarks.get(bench + "_js").items():
            m = calc_mean(b)
            n = browser + '-js'
            result.append([n, k, m])

        
        for k, b in benchmarks.get(bench + "_wasm").items():
            m = calc_mean(b)
            n = browser + '-wasm'
            result.append([n, k, m])

    df = DataFrame(result, columns=[bench, 'size', 'time'])

    df = df.pivot(index='size', columns=bench, values='time')

    df.plot()

    plt.xlabel('Array size (length)')

    if log == True:
        plt.ylabel('Execution time (ms), log-scale')
        plt.yscale('log')
        plt.tight_layout()
        fn = "../analysis/timeseries_" + device + "_" + bench + "_log.png"
        plt.savefig(fn, dpi=300, format="png")
    else:
        plt.ylabel('Execution time (ms)')
        plt.tight_layout()
        fn = "../analysis/timeseries_" + device + "_" + bench + "_nolog.png"
        plt.savefig(fn, dpi=300, format="png")


def time_series_graph(data, device, bench, log):
    result = []

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        for k, b in benchmarks.get(bench + "_js").items():
            m = calc_mean(b)
            n = browser + '-js'
            t = int(k.split("x")[0])
            result.append([n, t, m])

        
        for k, b in benchmarks.get(bench + "_wasm").items():
            m = calc_mean(b)
            n = browser + '-wasm'
            t = int(k.split("x")[0])
            result.append([n, t, m])

    df = DataFrame(result, columns=[bench, 'size', 'time'])

    df = df.pivot(index='size', columns=bench, values='time')

    df.plot()

    plt.xlabel('Quadratic maze size WxH (cells)')

    if log == True:
        plt.ylabel('Execution time (ms), log-scale')
        plt.yscale('log')
        plt.tight_layout()
        fn = "../analysis/timeseries_" + device + "_" + bench + "_log.png"
        plt.savefig(fn, dpi=300, format="png")
    else:
        plt.ylabel('Execution time (ms)')
        plt.tight_layout()
        fn = "../analysis/timeseries_" + device + "_" + bench + "_nolog.png"
        plt.savefig(fn, dpi=300, format="png")
