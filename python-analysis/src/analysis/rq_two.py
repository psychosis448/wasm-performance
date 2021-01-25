import matplotlib.pyplot as plt
from numpy import arange, std, mean, median
from pandas import DataFrame

def get_durations(benchmark):
    return list(map(lambda x : x['duration'], benchmark))

def calc_stdev(js):
    js_durations = get_durations(js)
    return std(js_durations)

# https://stackoverflow.com/questions/16592222/matplotlib-group-boxplots
def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)

def rq_two_js(mongo, device, arr_size, maze_size):
    data = mongo.db[device].find({ })

    result = dict()
    browsers = set([])

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')
        browsers.add(browser)

        result[browser] = []

        result[browser].append(get_durations(
            benchmarks.get("quicksort_int32array" + "_js").get(arr_size)))

        result[browser].append(get_durations(
            benchmarks.get("fmr" + "_js").get(arr_size)))

        result[browser].append(get_durations(
            benchmarks.get("bst_create" + "_js").get(arr_size)))

        # result[browser].append(get_durations(
        #     benchmarks.get("graph_create" + "_js").get(maze_size)))

        result[browser].append(get_durations(
            benchmarks.get("graph_solve" + "_js").get(maze_size)))

    plt.figure()

    for res in result:

        color = ""
        if res.__contains__("Safari"):
            color = "tab:red"
        elif res.startswith("Firefox"):
            color = "tab:orange"
        elif res.startswith("Chrome"):
            color = "tab:blue"
        elif res.startswith("Edge"):
            color = "tab:green"
        elif res.startswith("Samsung"):
            color = "tab:brown"

        pl = plt.boxplot(result[res],widths=0.6)

        set_box_color(pl, color)

    ticks = ["qs_int_arr"]

    for b in browsers:
        color = ""
        if b.__contains__("Safari"):
            color = "tab:red"
        elif b.startswith("Firefox"):
            color = "tab:orange"
        elif b.startswith("Chrome"):
            color = "tab:blue"
        elif b.startswith("Edge"):
            color = "tab:green"
        elif b.startswith("Samsung"):
            color = "tab:brown"

        plt.plot([], c=color, label=b)
    
    plt.legend()

    index=["qs", "fmr", "bst_create", "graph_solve"]

    plt.xticks(arange(1, len(index) + 1, step=1), index)
    plt.ylabel("Execution time in ms, log")
    plt.yscale('log')
    plt.tight_layout()

    plt.tight_layout()

    fn = "../analysis/distribution_" + device + "_js.png"
    plt.savefig(fn, dpi=300, format="png")

def rq_two_wasm(mongo, device, arr_size, maze_size):
    data = mongo.db[device].find({ })

    result = dict()
    browsers = set([])

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')
        browsers.add(browser)

        result[browser] = []

        result[browser].append(get_durations(
            benchmarks.get("quicksort_int32array" + "_wasm").get(arr_size)))

        result[browser].append(get_durations(
            benchmarks.get("fmr" + "_wasm").get(arr_size)))

        result[browser].append(get_durations(
            benchmarks.get("bst_create" + "_wasm").get(arr_size)))

        # result[browser].append(get_durations(
        #     benchmarks.get("graph_create" + "_wasm").get(maze_size)))

        result[browser].append(get_durations(
            benchmarks.get("graph_solve" + "_wasm").get(maze_size)))

    plt.figure()

    for res in result:

        color = ""
        if res.__contains__("Safari"):
            color = "tab:red"
        elif res.startswith("Firefox"):
            color = "tab:orange"
        elif res.startswith("Chrome"):
            color = "tab:blue"
        elif res.startswith("Edge"):
            color = "tab:green"
        elif res.startswith("Samsung"):
            color = "tab:brown"

        pl = plt.boxplot(result[res],widths=0.6)

        set_box_color(pl, color)

    for b in browsers:
        color = ""
        if b.__contains__("Safari"):
            color = "tab:red"
        elif b.startswith("Firefox"):
            color = "tab:orange"
        elif b.startswith("Chrome"):
            color = "tab:blue"
        elif b.startswith("Edge"):
            color = "tab:green"
        elif b.startswith("Samsung"):
            color = "tab:brown"

        plt.plot([], c=color, label=b)
    
    plt.legend()

    index=["qs", "fmr", "bst_create", "graph_solve"]

    plt.xticks(arange(1, len(index) + 1, step=1), index)
    plt.ylabel("Execution time in ms, log")
    plt.yscale('log')
    plt.tight_layout()

    plt.tight_layout()

    fn = "../analysis/distribution_" + device + "_wasm.png"
    plt.savefig(fn, dpi=300, format="png")


def rq_two_std(mongo, device, arr_size, maze_size, target):
    data = mongo.db[device].find({ })

    result = dict()

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        result[browser] = []

        result[browser].append(calc_stdev(
            benchmarks.get("quicksort_int32array" + "_" + target).get(arr_size)))

        result[browser].append(calc_stdev(
            benchmarks.get("fmr" + "_" + target).get(arr_size)))

        result[browser].append(calc_stdev(
            benchmarks.get("bst_create" + "_" + target).get(arr_size)))

        result[browser].append(calc_stdev(
            benchmarks.get("graph_create" + "_" + target).get(maze_size)))

        result[browser].append(calc_stdev(
            benchmarks.get("graph_solve" + "_" + target).get(maze_size)))

    data_frame = DataFrame(data=result,
        index=["qs", "fmr", "bst_create", "graph_create", "graph_solve"]
    )

    latex_table = data_frame.to_latex(float_format="%.2f", caption="Standard deviation for " + target + " on " + "device", label="tab:std-" + device + "-" + target)

    f = open("../analysis/std_" + device + "_"  + target + ".tex", "w")
    f.write(latex_table)
    f.close()
