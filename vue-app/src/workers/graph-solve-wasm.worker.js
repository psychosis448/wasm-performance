onmessage = async (message) => {
    const result = {};
    const { iterations, name, testData: data } = message.data;

    console.log(`Worker ${name} running...`);

    // method import
    const wasm = await import("../../wasm-pkg/index.js");
    const Graph = wasm.Graph
    //

    Object.entries(data).forEach(([key, value]) => {
        const dataId = `${key}`;

        // prep
        const [rows, columns] = dataId.split('x')
        const graph = new Graph(+rows, +columns)
        graph.set_maze_from_js(value)
        //

        for (let i = 0; i < iterations; i++) {
            performance.mark(`${name}-${dataId}-${i}-start`);

            // execute
            graph.solve_maze()
            //

            performance.mark(`${name}-${dataId}-${i}-end`);
            performance.measure(
                `${name}-${dataId}-${i}`,
                `${name}-${dataId}-${i}-start`,
                `${name}-${dataId}-${i}-end`
            );
        }

        // tear down
        graph.free()
        //

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
