from numpy import std, mean, median
from pandas import DataFrame
from statistics import geometric_mean
import matplotlib.pyplot as plt

def get_durations(benchmark):
    return list(map(lambda x : x['duration'], benchmark))

def calc_speedup(js, wasm):
    js_durations = get_durations(js)
    wasm_durations = get_durations(wasm)

    js_mean = mean(js_durations)
    wasm_mean = mean(wasm_durations)

    return js_mean / wasm_mean

def calc_stdev(js):
    js_durations = get_durations(js)
    return std(js_durations)

def calc_mean(js):
    js_durations = get_durations(js)
    return mean(js_durations)

def rq_one(mongo, device, arr_size, maze_size):
    data = mongo.db[device].find({})

    result = dict()
    stdev = dict()

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        result[browser] = []
        stdev[browser] = []

        # quicksort_int32array
        result[browser].append(calc_speedup(
            benchmarks.get("quicksort_int32array" + "_js").get(arr_size),
            benchmarks.get("quicksort_int32array" + "_wasm").get(arr_size)))
    
        # quicksort_array
        result[browser].append(calc_speedup(
            benchmarks.get("quicksort_array" + "_js").get(arr_size),
            benchmarks.get("quicksort_array" + "_wasm").get(arr_size)))

        # fmr
        result[browser].append(calc_speedup(
            benchmarks.get("fmr" + "_js").get(arr_size),
            benchmarks.get("fmr" + "_wasm").get(arr_size)))

        # fmr_jsvalue
        result[browser].append(calc_speedup(
            benchmarks.get("fmr" + "_js").get(arr_size),
            benchmarks.get("fmr_jsvalue" + "_wasm").get(arr_size)))

        # bst_create
        result[browser].append(calc_speedup(
            benchmarks.get("bst_create" + "_js").get(arr_size),
            benchmarks.get("bst_create" + "_wasm").get(arr_size)))

        # graph_create
        result[browser].append(calc_speedup(
            benchmarks.get("graph_create" + "_js").get(maze_size),
            benchmarks.get("graph_create" + "_wasm").get(maze_size)))

        # graph_solve
        result[browser].append(calc_speedup(
            benchmarks.get("graph_solve" + "_js").get(maze_size),
            benchmarks.get("graph_solve" + "_wasm").get(maze_size)))

    # create data frame
    plot_data = DataFrame(
        result,
        index=["qs_int_arr", "qs_arr", "fmr", "fmr_jsval", "bst_create", "graph_create", "graph_solve"]
    )

    # plot data
    plot_data.plot(kind="bar", color={
            "Safari": "tab:red",
            "Mobile Safari": "tab:red",
            "Firefox": "tab:orange",
            "Chrome": "tab:blue",
            "Edge": "tab:green",
            "Samsung Browser": "tab:brown"
        })

    plt.ylabel('Speed up (relative to JS)')
    plt.xticks(rotation=15, horizontalalignment="center")
    plt.axhline(y=1.0, color='black', linestyle='--', linewidth=0.7)

    plt.tight_layout()

    fn = "../analysis/speedup_" + device + ".png"
    plt.savefig(fn, dpi=300, format="png")

def rq_one_table(mongo, device, arr_size, maze_size):
    data = mongo.db[device].find({})

    result = dict()

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        result[browser] = []

        # quicksort_int32array
        result[browser].append(calc_speedup(
            benchmarks.get("quicksort_int32array" + "_js").get(arr_size),
            benchmarks.get("quicksort_int32array" + "_wasm").get(arr_size)))

        # quicksort_array
        result[browser].append(calc_speedup(
            benchmarks.get("quicksort_array" + "_js").get(arr_size),
            benchmarks.get("quicksort_array" + "_wasm").get(arr_size)))

        # fmr
        result[browser].append(calc_speedup(
            benchmarks.get("fmr" + "_js").get(arr_size),
            benchmarks.get("fmr" + "_wasm").get(arr_size)))

        # fmr_jsvalue
        result[browser].append(calc_speedup(
            benchmarks.get("fmr" + "_js").get(arr_size),
            benchmarks.get("fmr_jsvalue" + "_wasm").get(arr_size)))

        # bst_create
        result[browser].append(calc_speedup(
            benchmarks.get("bst_create" + "_js").get(arr_size),
            benchmarks.get("bst_create" + "_wasm").get(arr_size)))

        # graph_create
        result[browser].append(calc_speedup(
            benchmarks.get("graph_create" + "_js").get(maze_size),
            benchmarks.get("graph_create" + "_wasm").get(maze_size)))

        # graph_solve
        result[browser].append(calc_speedup(
            benchmarks.get("graph_solve" + "_js").get(maze_size),
            benchmarks.get("graph_solve" + "_wasm").get(maze_size)))

        g_mean = geometric_mean(result[browser])
        m = median(result[browser])

        result[browser].append(g_mean)
        result[browser].append(m)

    # create data frame
    data_frame = DataFrame(
        result,
        index=["qs_int_arr", "qs_arr", "fmr", "fmr_jsval", "bst_create", "graph_create", "graph_solve", "geomean", "median"]
    )

    latex_table = data_frame.to_latex(float_format="%.2f", caption="WebAssembly speedup relative to JavaScript on " + device + ".", label="speedup-" + device)

    f = open("../analysis/speedup_" + device + ".tex", "w")
    f.write(latex_table)
    f.close()

def rq_one_js(mongo, device, arr_size, maze_size):
    data = mongo.db[device].find({})

    result = dict()
    stdev = dict()

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        result[browser] = []
        stdev[browser] = []

        # quicksort_int32array
        result[browser].append(calc_mean(
            benchmarks.get("quicksort_int32array" + "_js").get(arr_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("quicksort_int32array" + "_js").get(arr_size)))

        # quicksort_array
        result[browser].append(calc_mean(
            benchmarks.get("quicksort_array" + "_js").get(arr_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("quicksort_array" + "_js").get(arr_size)))

        # fmr
        result[browser].append(calc_mean(
            benchmarks.get("fmr" + "_js").get(arr_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("fmr" + "_js").get(arr_size)))

        # bst_create
        result[browser].append(calc_mean(
            benchmarks.get("bst_create" + "_js").get(arr_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("bst_create" + "_js").get(arr_size)))

        # graph_create
        result[browser].append(calc_mean(
            benchmarks.get("graph_create" + "_js").get(maze_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("graph_create" + "_js").get(maze_size)))

        # graph_solve
        result[browser].append(calc_mean(
            benchmarks.get("graph_solve" + "_js").get(maze_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("graph_solve" + "_js").get(maze_size)))


    # create data frame
    plot_data = DataFrame(
        result,
        index=["qs_int_arr", "qs_arr", "fmr", "bst_create", "graph_create", "graph_solve"]
    )

    # plot data
    plot_data.plot(kind="bar", yerr=stdev, color={
            "Safari": "tab:red",
            "Mobile Safari": "tab:red",
            "Firefox": "tab:orange",
            "Chrome": "tab:blue",
            "Edge": "tab:green",
            "Samsung Browser": "tab:brown"
        })
    plt.ylabel('Execution times in ms')
    plt.xticks(rotation=15, horizontalalignment="center")
    
    plt.tight_layout()

    fn = "../analysis/js_" + device + ".png"
    plt.savefig(fn, dpi=300, format="png")

def rq_one_wasm(mongo, device, arr_size, maze_size):
    data = mongo.db[device].find({})

    result = dict()
    stdev = dict()

    for d in data:
        benchmarks = d.get('benchmarks')
        browser = d.get('ua').get('browser').get('name')

        result[browser] = []
        stdev[browser] = []

        # quicksort_int32array
        result[browser].append(calc_mean(
            benchmarks.get("quicksort_int32array" + "_wasm").get(arr_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("quicksort_int32array" + "_wasm").get(arr_size)))

        # quicksort_array
        result[browser].append(calc_mean(
            benchmarks.get("quicksort_array" + "_wasm").get(arr_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("quicksort_array" + "_wasm").get(arr_size)))

        # fmr
        result[browser].append(calc_mean(
            benchmarks.get("fmr" + "_wasm").get(arr_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("fmr" + "_wasm").get(arr_size)))

        # fmr_jsvalue
        result[browser].append(calc_mean(
            benchmarks.get("fmr_jsvalue" + "_wasm").get(arr_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("fmr_jsvalue" + "_wasm").get(arr_size)))

        # bst_create
        result[browser].append(calc_mean(
            benchmarks.get("bst_create" + "_wasm").get(arr_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("bst_create" + "_wasm").get(arr_size)))

        # graph_create
        result[browser].append(calc_mean(
            benchmarks.get("graph_create" + "_wasm").get(maze_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("graph_create" + "_wasm").get(maze_size)))

        # graph_solve
        result[browser].append(calc_mean(
            benchmarks.get("graph_solve" + "_wasm").get(maze_size)))
    
        stdev[browser].append(calc_stdev(
            benchmarks.get("graph_solve" + "_wasm").get(maze_size)))

    # create data frame
    plot_data = DataFrame(
        result,
        index=["qs_int_arr", "qs_arr", "fmr", "fmr_jsvalue", "bst_create", "graph_create", "graph_solve"]
    )

    # plot data
    plot_data.plot(kind="bar", yerr=stdev, color={
            "Safari": "tab:red",
            "Mobile Safari": "tab:red",
            "Firefox": "tab:orange",
            "Chrome": "tab:blue",
            "Edge": "tab:green",
            "Samsung Browser": "tab:brown"
        })

    plt.ylabel('Execution times in ms')
    plt.xticks(rotation=15, horizontalalignment="center")

    plt.tight_layout()

    fn = "../analysis/wasm_" + device + ".png"
    plt.savefig(fn, dpi=300, format="png")