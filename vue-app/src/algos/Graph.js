const PriorityQueue = require('priorityqueuejs');

// improve readability
PriorityQueue.prototype.has = function (value) {
  return this._elements.find(el => el.value === value) !== undefined
}

const formatValue = (x, y) => `${x},${y}`

class Vertex {
  constructor({ x, y }) {
    this.value = formatValue(x, y)
    this.x = x
    this.y = y
  }

  getNeighbors(columns, rows) {
    const neighbors = new Array();

    if (this.y > 0) neighbors.push(formatValue(this.x, this.y - 1))
    if (this.y < rows - 1) neighbors.push(formatValue(this.x, this.y + 1))
    if (this.x > 0) neighbors.push(formatValue(this.x - 1, this.y))
    if (this.x < columns - 1) neighbors.push(formatValue(this.x + 1, this.y))

    return neighbors
  }
}

export class Graph {
  constructor({ rows, columns }) {
    this.rows = rows
    this.columns = columns
    this.startVertex = formatValue(0, 0)
    this.endVertex = formatValue(columns - 1, rows - 1)
    this.vertices = new Map()
    this.edges = new Map()

    for (let x = 0; x < rows; x++) {
      for (let y = 0; y < columns; y++) {
        this.vertices.set(formatValue(x, y), new Vertex({ x, y }))
      }
    }
  }

  getStart() {
    return this.startVertex
  }

  getEnd() {
    return this.endVertex
  }

  setMazeFromWasm(maze) {
    this.rows = maze.rows
    this.columns = maze.columns
    this.startVertex = maze.start_vertex || maze.startVertex
    this.endVertex = maze.end_vertex || maze.endVertex
    this.vertices = new Map(Object.entries(maze.vertices))
    this.edges = new Map(Object.entries(maze.edges))
  }

  createMaze() {
    this.edges = this.primMaze()
  }

  getMaze() {
    return this.edges
  }

  solveMaze() {
    return this.aStar()
  }

  getVertex(value) {
    return this.vertices.get(value)
  }

  getEdge(value) {
    return this.edges.get(value)
  }

  primMaze() {
    const pathSet = new Set()
    const visited = new Set()
    const edges = new Map()

    this.vertices.forEach((_, key) => edges.set(key, []))

    this.getVertex(this.startVertex)
      .getNeighbors(this.columns, this.rows)
      .forEach(neighbor => pathSet.add(neighbor))

    visited.add(this.startVertex)

    while (pathSet.size > 0) {
      const paths = Array.from(pathSet)
      const randV = Math.floor(Math.random() * pathSet.size)
      const randomPath = paths[randV]
      const currentVertex = this.getVertex(randomPath)
      visited.add(currentVertex.value)

      const currentNeighbors = currentVertex.getNeighbors(this.columns, this.rows)
      const availableNeighbors = []

      currentNeighbors.forEach(neighbor => {
        if (visited.has(neighbor)) {
          availableNeighbors.push(neighbor)
        } else {
          pathSet.add(neighbor)
        }
      })

      if (availableNeighbors.length > 0) {
        const randN = Math.floor(Math.random() * availableNeighbors.length)
        const newEdge = availableNeighbors[randN]

        edges.get(currentVertex.value).push(newEdge)
        edges.get(newEdge).push(currentVertex.value)
      }

      pathSet.delete(currentVertex.value)
    }

    return edges
  }

  aStar() {
    const start = this.startVertex
    const end = this.endVertex
    const endVertex = this.getVertex(this.endVertex)

    const openQueue = new PriorityQueue((a, b) => b.f - a.f)
    const closedSet = new Set()
    const gScores = new Map()
    const parents = new Map()

    this.edges.forEach((_, edge) => {
      if (edge !== start) {
        gScores.set(edge, Infinity)
      } else {
        gScores.set(edge, 0)
      }
    })

    openQueue.enq({ f: 0, value: start })

    while (!openQueue.isEmpty()) {
      const currentVertex = openQueue.deq()

      if (currentVertex.value === end) {
        const path = new Array()
        let next = currentVertex.value
        path.push(next)

        while (next !== start) {
          const child = parents.get(next)
          path.push(child)
          next = child
        }

        path.reverse()

        return path
      }

      closedSet.add(currentVertex.value)

      const gScore = gScores.get(currentVertex.value) + 1

      this.getEdge(currentVertex.value).forEach((edge) => {
        if (!closedSet.has(edge)) {
          const edgeG = gScores.get(edge)

          if (gScore < edgeG) {
            const edgeVertex = this.getVertex(edge)
            const edgeH = this.manhattanDistance(edgeVertex, endVertex)
            const edgeF = gScore + edgeH

            gScores.set(edge, gScore)
            openQueue.enq({ f: edgeF, value: edge })
            parents.set(edge, currentVertex.value)
          }
        }
      })
    }

    return null
  }

  manhattanDistance(vertex, destination) {
    const d1 = Math.abs(destination.x - vertex.x)
    const d2 = Math.abs(destination.y - vertex.y)
    return d1 + d2
  }
}