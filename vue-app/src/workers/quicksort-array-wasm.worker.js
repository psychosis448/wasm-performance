onmessage = async (message) => {
    const result = {};
    const { iterations, name, testData: data } = message.data;

    console.log(`Worker ${name} running...`);

    // method import
    const wasm = await import("../../wasm-pkg/index.js");
    const quicksort = wasm.quicksort_vec
    //

    Object.entries(data).forEach(([key, value]) => {
        const dataId = `${key}`;

        for (let i = 0; i < iterations; i++) {
            // setup
            const array = [...value]
            //

            performance.mark(`${name}-${dataId}-${i}-start`);

            // execute
            quicksort(array)
            //

            performance.mark(`${name}-${dataId}-${i}-end`);
            performance.measure(
                `${name}-${dataId}-${i}`,
                `${name}-${dataId}-${i}-start`,
                `${name}-${dataId}-${i}-end`
            );

            // tear down
            //
            //
        }

        result[dataId] = performance.getEntriesByType("measure").map(m => {
            return {
                name: m.name,
                duration: m.duration,
                startTime: m.startTime,
                entryType: m.entryType
            }
        });

        performance.clearMarks();
        performance.clearMeasures();
    });

    console.log(`...${name} worker done.`);

    postMessage({ result, name });
}
