onmessage = async (message) => {
    const result = {};
    const { iterations, name, testData: data } = message.data;

    console.log(`Worker ${name} running...`)

    // method import
    const { Graph } = await import("../algos/Graph.js")
    //

    Object.entries(data).forEach(([key, value]) => {
        const dataId = `${key}`;

        // prep
        const { rows, columns } = value;
        //

        for (let i = 0; i < iterations; i++) {
            // setup
            const graph = new Graph({ rows, columns });
            //

            performance.mark(`${name}-${dataId}-${i}-start`);

            // execute
            graph.createMaze();
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

    console.log(`...${name} worker done.`)

    postMessage({ result, name })
}
