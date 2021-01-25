from statistics import mean, median
from numpy import std
from pandas import DataFrame

def cmp_e_c (mongo):
    browser = mongo.db['desktop'].find({ '$or': [
        { "ua.browser.name": 'Chrome'},
        {"ua.browser.name": 'Edge'}
    ] })

    benchmarks = browser[0].get('benchmarks').keys()

    results = []

    for benchmark in benchmarks:
        chrome = browser[0].get('benchmarks').get(benchmark)
        edge = browser[1].get('benchmarks').get(benchmark)

        keys = chrome.keys()

        for key in keys:
            chrome_durations = list(map(lambda x : x['duration'], chrome.get(key)))
            edge_durations = list(map(lambda x : x['duration'], edge.get(key)))

            # mean or median
            chrome_mean = median(chrome_durations)
            edge_mean = median(edge_durations)
            diff = (chrome_mean - edge_mean)
            std_deviation = std([chrome_mean, edge_mean])

            percent = 100 * diff / chrome_mean

            results.append(dict(benchmark=benchmark, size=key, cm=chrome_mean, em=edge_mean, sd=std_deviation, p=percent))

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
    data_frame = DataFrame(data=results)
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_latex.html
    latex_table = data_frame.to_latex(float_format="%.4f", longtable=True, caption="Arithmetic means and standard deviation for Chrome and Edge.", label="ltab:c-e-std")

    f = open("../analysis/chrome-edge-std.tex", "w")
    f.write(latex_table)
    f.close()
