<template>
  <div class="container">
    <h2>Benchmark</h2>
    <router-link to="/maze-wasm" tag="button">Maze-Wasm</router-link>
    <router-link to="/maze-js" tag="button">Maze-JS</router-link>
    <div class="container-content">
      <table>
        <thead>
          <th>Benchmark</th>
          <th>Status</th>
        </thead>
        <tbody>
          <tr v-for="benchmark in benchmarkConfig" :key="benchmark.name">
            <td>{{ benchmark.name }}</td>
            <td>
              <span
                v-if="benchmark.status !== BENCHMARK_STATUS.RUNNING"
                :class="benchmark.status"
              >
                {{ benchmark.status }}</span
              >
              <Spinner v-else />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div>
      <h2>Status</h2>
      <div>done : {{ BENCHMARK_DONE }}</div>
      <div>running : {{ BENCHMARK_ACTIVE }}</div>
    </div>
    <div>
      <h2>Features</h2>
      <ul>
        <li>worker : {{ webWorker }}</li>
        <li v-for="(value, propertyName) in wasmFeatures" :key="propertyName">
          {{ propertyName }} : {{ value }}
        </li>
      </ul>
    </div>
    <br />
    <div class="container-content">
      <p v-if="device.length === 0" style="color: red">
        Please insert device details first.
      </p>
      <button
        @click="
          start();
          BENCHMARK_RUNNING = !BENCHMARK_RUNNING;
        "
        :disabled="BENCHMARK_RUNNING || device.length === 0"
      >
        Run Benchmarks
      </button>
    </div>
    <div class="container-content">
      <label for="device">Device </label>
      <input type="text" id="device" name="device" v-model="device" />
    </div>
    <div class="container-content">
      <label for="details">Details </label>
      <input type="text" id="details" name="details" v-model="details" />
    </div>
    <div class="container-content">
      <a download="result.json" id="download-button">
        <button :disabled="!BENCHMARK_DONE || device.length === 0">
          Download Results
        </button>
      </a>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import { computed, reactive, ref, watch } from "vue";
import Spinner from "@/views/Spinner";
import HTTP from "@/util/HTTP";
import { BENCHMARK_STATUS } from "@/util/CONSTANTS";
import { Benchmark } from "@/util/Benchmark";
import { createBlob } from "@/util/createBlob";
// WORKERS
// quicksort
import QuicksortInt32ArrayWorkerJs from "@/workers/quicksort-int32array-js.worker.js";
import QuicksortInt32ArrayWorkerWasm from "@/workers/quicksort-int32array-wasm.worker.js";
import QuicksortArrayWorkerJs from "@/workers/quicksort-array-js.worker.js";
import QuicksortArrayWorkerWasm from "@/workers/quicksort-array-wasm.worker.js";
// filter map reduce
import FmrWorkerJs from "@/workers/fmr-js.worker.js";
import FmrWorkerWasm from "@/workers/fmr-wasm.worker.js";
import FmrJsValueWorkerWasm from "@/workers/fmr-jsvalue-wasm.worker.js";
// // binary search tree
import BstCreateWorkerJs from "@/workers/bst-create-js.worker.js";
import BstCreateWorkerWasm from "@/workers/bst-create-wasm.worker.js";
// // graph
import GraphCreateWorkerJs from "@/workers/graph-create-js.worker.js";
import GraphCreateWorkerWasm from "@/workers/graph-create-wasm.worker.js";
import GraphSolveWorkerJs from "@/workers/graph-solve-js.worker.js";
import GraphSolveWorkerWasm from "@/workers/graph-solve-wasm.worker.js";

export default {
  name: "BenchRun",
  components: { Spinner },
  async setup() {
    const device = ref("");
    const details = ref("");

    const iterations = 30;
    const benchmark = new Benchmark({ iterations });

    const benchmarkConfig = reactive({
      // quicksort
      quicksort_int32array_js: {
        name: "quicksort_int32array_js",
        status: BENCHMARK_STATUS.IDLE,
        worker: new QuicksortInt32ArrayWorkerJs(),
        testData: "unsorted",
      },
      quicksort_int32array_wasm: {
        name: "quicksort_int32array_wasm",
        status: BENCHMARK_STATUS.IDLE,
        worker: new QuicksortInt32ArrayWorkerWasm(),
        testData: "unsorted",
      },
      quicksort_array_js: {
        name: "quicksort_array_js",
        status: BENCHMARK_STATUS.IDLE,
        worker: new QuicksortArrayWorkerJs(),
        testData: "unsorted",
      },
      quicksort_array_wasm: {
        name: "quicksort_array_wasm",
        status: BENCHMARK_STATUS.IDLE,
        worker: new QuicksortArrayWorkerWasm(),
        testData: "unsorted",
      },
      // filter map reduce
      fmr_js: {
        name: "fmr_js",
        status: BENCHMARK_STATUS.IDLE,
        worker: new FmrWorkerJs(),
        testData: "unsorted",
      },
      fmr_wasm: {
        name: "fmr_wasm",
        status: BENCHMARK_STATUS.IDLE,
        worker: new FmrWorkerWasm(),
        testData: "unsorted",
      },
      fmr_jsvalue_wasm: {
        name: "fmr_jsvalue_wasm",
        status: BENCHMARK_STATUS.IDLE,
        worker: new FmrJsValueWorkerWasm(),
        testData: "unsorted",
      },
      // // binary search tree
      bst_create_js: {
        name: "bst_create_js",
        status: BENCHMARK_STATUS.IDLE,
        worker: new BstCreateWorkerJs(),
        testData: "unsorted",
      },
      bst_create_wasm: {
        name: "bst_create_wasm",
        status: BENCHMARK_STATUS.IDLE,
        worker: new BstCreateWorkerWasm(),
        testData: "unsorted",
      },
      // graph
      graph_create_js: {
        name: "graph_create_js",
        status: BENCHMARK_STATUS.IDLE,
        worker: new GraphCreateWorkerJs(),
        testData: "graphCreate",
      },
      graph_create_wasm: {
        name: "graph_create_wasm",
        status: BENCHMARK_STATUS.IDLE,
        worker: new GraphCreateWorkerWasm(),
        testData: "graphCreate",
      },
      graph_solve_js: {
        name: "graph_solve_js",
        status: BENCHMARK_STATUS.IDLE,
        worker: new GraphSolveWorkerJs(),
        testData: "graphSolve",
      },
      graph_solve_wasm: {
        name: "graph_solve_wasm",
        status: BENCHMARK_STATUS.IDLE,
        worker: new GraphSolveWorkerWasm(),
        testData: "graphSolve",
      },
    });

    // ui reactivity etc.
    const start = async () => {
      await benchmarkRunner.next();
    };

    const BENCHMARK_RUNNING = ref(false);
    const BENCHMARK_ACTIVE = ref(false);

    watch(BENCHMARK_ACTIVE, async (BENCHMARK_ACTIVE) => {
      if (!BENCHMARK_ACTIVE) {
        await benchmarkRunner.next();
      }
    });

    const BENCHMARK_DONE = computed(() => {
      return (
        Object.values(benchmarkConfig).filter(
          (x) => x.status !== BENCHMARK_STATUS.DONE
        ).length === 0
      );
    });

    watch(BENCHMARK_DONE, (BENCHMARK_DONE) => {
      if (BENCHMARK_DONE) {
        benchmark.setInfo({ device: device.value, details: details.value });
        benchmark.setFeatures(window.wasmFeatures);
        createBlob(benchmark);
      }
    });

    // data
    const { data: unsorted } = await HTTP.get("/unsorted");
    const { data: graphCreate } = await HTTP.get("/graph-create");
    const { data: graphSolve } = await HTTP.get("/graph-solve");

    const benchmarkData = {
      unsorted: unsorted,
      graphCreate: graphCreate,
      graphSolve: graphSolve,
    };

    // benchmark runner
    const benchmarkRunner = runBenchmarks();

    // generator function to step through benchmarks
    async function* runBenchmarks() {
      if (!BENCHMARK_DONE.value) {
        for (const [key, value] of Object.entries(benchmarkConfig)) {
          await new Promise((resolve) => {
            const worker = value.worker;
            worker.onerror = (e) => console.log(e);
            worker.onmessage = ({ data }) => {
              const result = { name: data.name, data: data.result };
              benchmark.setResult(result);
              benchmarkConfig[key].status = BENCHMARK_STATUS.DONE;
              BENCHMARK_ACTIVE.value = false;
              resolve(result);
            };

            BENCHMARK_ACTIVE.value = true;
            benchmarkConfig[key].status = BENCHMARK_STATUS.RUNNING;

            worker.postMessage({
              iterations,
              name: value.name,
              testData: benchmarkData[value.testData],
            });
          });

          yield key;
        }
      }
    }

    // additional info
    const wasmFeatures = window.wasmFeatures;
    const webWorker = typeof Worker !== undefined;

    return {
      BENCHMARK_STATUS,
      BENCHMARK_ACTIVE,
      BENCHMARK_DONE,
      BENCHMARK_RUNNING,
      benchmarkConfig,
      start,
      device,
      details,
      wasmFeatures,
      webWorker,
    };
  },
};
</script>

<style >
table,
th,
td {
  border: 1px solid black;
  border-collapse: collapse;
}

th,
td {
  padding: 0.5rem;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.container-content {
  margin: 0.3rem;
}

.idle {
  color: red;
}

.done {
  color: green;
}
</style>