import json
from data_base.mongo import MongoDB
from analysis.rq_one import rq_one, rq_one_table, rq_one_js, rq_one_wasm
from analysis.rq_two import rq_two_js, rq_two_wasm, rq_two_std
from analysis.rq_three import rq_three
from analysis.rq_four import rq_four

devices = ['desktop', 'macbook', 'smartphone']

def main():
    mongo = MongoDB()
    mongo.start()
    mongo.connect()
    mongo.connect_db("benchmarks")

    # read data into mongodb
    for device in devices:
        mongo.add_json_data(device)

    # process data
    for device in devices:
        print("[analysis] processing data for", device)

        arr_size = str(pow(10,5))
        maze_size = ""

        if device == "smartphone":
            maze_size="50x50"
        else:
            maze_size="150x150"

    # RQ1: What is the performance difference between JavaScript and WebAssembly across different browsers?
        print("[rq_1] processing")
        rq_one(mongo, device, arr_size, maze_size)
        rq_one_table(mongo, device, arr_size, maze_size)
        rq_one_js(mongo, device, arr_size, maze_size)
        rq_one_wasm(mongo, device, arr_size, maze_size)

    # RQ2: How big is the execution time spread for JavaScript and WebAssembly per function across different browsers?
        print("[rq_2] processing")
        rq_two_js(mongo, device, arr_size, maze_size)
        rq_two_wasm(mongo, device, arr_size, maze_size)
        rq_two_std(mongo, device, arr_size, maze_size, target="wasm")
        rq_two_std(mongo, device, arr_size, maze_size, target="js")

    # RQ3: How does the performance change for increasing payloads for WebAssembly and JavaScript?
        print("[rq_3] processing")
        rq_three(mongo, device, log=True)
        rq_three(mongo, device, log=False)

    # RQ4: How large is the introduced overhead for copy and/or serialization operations and to what extend is this influenced by input size?
        print("[rq_4] processing")
        rq_four(mongo, device, log=True)
        rq_four(mongo, device, log=False)

if __name__ == "__main__":
    main()
