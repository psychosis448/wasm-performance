const Graph = require('./Graph')

const createMazes = (data) => {
    const mazes = {}

    Object.entries(data).forEach(([key, value]) => {
        const { rows, columns } = value;
        const graph = new Graph({ rows, columns })

        graph.createMaze()

        graph.edges = Object.fromEntries(graph.edges)
        graph.vertices = Object.fromEntries(graph.vertices)

        mazes[key] = graph
    })

    return mazes
}
module.exports = createMazes
