from numpy import std, mean, median
from pandas import DataFrame, Series
from statistics import geometric_mean
import matplotlib.pyplot as plt

color = {
    "Safari": "tab:red",
    "Mobile Safari": "tab:red",
    "Firefox": "tab:orange",
    "Chrome": "tab:blue",
    "Edge": "tab:green",
    "Samsung Browser": "tab:brown"
}

def get_durations(benchmark):
    return list(map(lambda x : x['duration'], benchmark))

def calc_speedup(wasm, wasm_serde):
    return wasm / wasm_serde

def calc_stdev(js):
    js_durations = get_durations(js)
    return std(js_durations)

def calc_mean(js):
    js_durations = get_durations(js)
    return mean(js_durations)

def rq_four(mongo, device, log):
    data = list(mongo.db[device].find({}))

    time_series_fmr(data, device, log)
    time_series_qs(data, device, log)

    if device != 'smartphone':
        rq_four_penalty_fmr(data, device)
        rq_four_penalty_arr(data, device)

def f_a(x):
    return "{:.2f}".format(x)

def rq_four_penalty_fmr(data, device):
    result = dict()

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        result[browser] = []

        fmr_wasm = []
        fmr_wasm_jsval = []

        for k, b in benchmarks.get("fmr_wasm").items():
            m = calc_mean(b)
            fmr_wasm.append(m)

        for k, b in benchmarks.get("fmr_jsvalue_wasm").items():
            m = calc_mean(b)
            fmr_wasm_jsval.append(m)

        for i, v in enumerate(fmr_wasm):
            fw = fmr_wasm[i]
            fv = fmr_wasm_jsval[i]
            s = Series([fw, fv])
            percentage = s.pct_change()
            p = f_a((percentage[1] * 100))
            result[browser].append(p)

    df = DataFrame(data=result,
        index=["10^1", "10^2", "10^3", "10^4", "10^5", "10^6"]
    )

    latex_table = df.to_latex(float_format="%.2f", caption="Performance slowdown through copy/serialize.", label="tab:overhead-slowdown")

    f = open("../analysis/slowdown_fmr_" + device + ".tex", "w")
    f.write(latex_table)
    f.close()

def rq_four_penalty_arr(data, device):
    result = dict()

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        result[browser] = []

        fmr_wasm = []
        fmr_wasm_jsval = []

        for k, b in benchmarks.get("quicksort_int32array_wasm").items():
            m = calc_mean(b)
            fmr_wasm.append(m)

        for k, b in benchmarks.get("quicksort_array_wasm").items():
            m = calc_mean(b)
            fmr_wasm_jsval.append(m)

        for i, v in enumerate(fmr_wasm):
            fw = fmr_wasm[i]
            fv = fmr_wasm_jsval[i]
            s = Series([fw, fv])
            percentage = s.pct_change()
            p = f_a((percentage[1] * 100))
            result[browser].append(p)

    data_frame = DataFrame(data=result,
        index=["10^1", "10^2", "10^3", "10^4", "10^5", "10^6"]
    )

    latex_table = data_frame.to_latex(float_format="%.2f", caption="Performance slowdown through copy/serialize.", label="tab:overhead-slowdown")

    f = open("../analysis/slowdown_qs_" + device + ".tex", "w")
    f.write(latex_table)
    f.close()

def time_series_fmr(data, device, log):
    result = []

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        for k, b in benchmarks.get("fmr_wasm").items():
            m = calc_mean(b)
            n = browser + '-wasm'
            result.append([n, k, m])

        for k, b in benchmarks.get("fmr_jsvalue_wasm").items():
            m = calc_mean(b)
            n = browser + '-serde-wasm'
            result.append([n, k, m])

    df = DataFrame(result, columns=['fmr', 'size', 'time'])

    df = df.pivot(index='size', columns='fmr', values='time')

    df.plot()

    plt.xlabel('Array size (length)')

    if log == True:
        plt.ylabel('Execution time (ms), log-scale')
        plt.yscale('log')
        plt.tight_layout()
        fn = "../analysis/overhead_" + device + "_fmr_log.png"
        plt.savefig(fn, dpi=300, format="png")
    else:
        plt.ylabel('Execution time (ms)')
        plt.tight_layout()
        fn = "../analysis/overhead_" + device + "_fmr_nolog.png"
        plt.savefig(fn, dpi=300, format="png")

def time_series_qs(data, device, log):
    result = []

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        for k, b in benchmarks.get("quicksort_int32array_wasm").items():
            m = calc_mean(b)
            n = browser + '-wasm'
            result.append([n, k, m])

        for k, b in benchmarks.get("quicksort_array_wasm").items():
            m = calc_mean(b)
            n = browser + '-serde-wasm'
            result.append([n, k, m])

    df = DataFrame(result, columns=['fmr', 'size', 'time'])

    df = df.pivot(index='size', columns='fmr', values='time')

    df.plot()

    plt.xlabel('Array size (length)')

    if log == True:
        plt.ylabel('Execution time (ms), log-scale')
        plt.yscale('log')
        plt.tight_layout()
        fn = "../analysis/overhead_" + device + "_qs_log.png"
        plt.savefig(fn, dpi=300, format="png")
    else:
        plt.ylabel('Execution time (ms)')
        plt.tight_layout()
        fn = "../analysis/overhead_" + device + "_qs_nolog.png"
        plt.savefig(fn, dpi=300, format="png")