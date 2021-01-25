import UAParser from "ua-parser-js";
import { v4 as uuidv4 } from "uuid";
const parser = new UAParser();

export class Benchmark {
    constructor(options = {}) {
        Object.assign(this, {
            uuid: uuidv4(),
            date: new Date(),
            ua: parser.getResult(),
            features: {
                webworker: typeof Worker !== undefined
            },
            info: {},
            iterations: 20,
            benchmarks: {}
        }, options)
    }

    setResult({ name, data }) {
        this.benchmarks[name] = data
    }

    setFeatures(wasmFeatures) {
        this.features.wasm = wasmFeatures
    }

    setInfo(info) {
        this.info = info
    }
}
