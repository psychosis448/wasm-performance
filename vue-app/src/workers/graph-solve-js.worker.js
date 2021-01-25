onmessage = async (message) => {
    const result = {};
    const { iterations, name, testData: data } = message.data;

    console.log(`Worker ${name} running...`);

    // method import
    const { Graph } = await import("../algos/Graph.js")
    //

    Object.entries(data).forEach(([key, value]) => {
        const dataId = `${key}`;

        // prep
        const [rows, columns] = dataId.split('x')
        const graph = new Graph({ rows, columns })
        graph.setMazeFromWasm(value)
        //

        for (let i = 0; i < iterations; i++) {
            performance.mark(`${name}-${dataId}-${i}-start`);

            // execute
            graph.solveMaze()
            //

            performance.mark(`${name}-${dataId}-${i}-end`);
            performance.measure(
                `${name}-${dataId}-${i}`,
                `${name}-${dataId}-${i}-start`,
                `${name}-${dataId}-${i}-end`
            );

            // tear down
            // TODO
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
