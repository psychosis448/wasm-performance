<template>
  <div>
    <h1>Maze</h1>
    <canvas id="maze"></canvas>
  </div>
</template>

<script>
import { onMounted } from "vue";
import { Graph } from "@/algos/Graph";
import { drawMaze, drawSolution } from "@/util/canvasDraw";

export default {
  name: "MazeJs",
  setup() {
    const columns = 20; // width
    const rows = 20; // height
    const cellWidth = 4;
    const width = columns * cellWidth;
    const height = rows * cellWidth;
    const offset = cellWidth / 2;
    const scale = 5;

    onMounted(() => {
      const canvas = document.getElementById("maze");
      const ctx = canvas.getContext("2d");
      canvas.height = (height - offset) * scale;
      canvas.width = (width - offset) * scale;

      drawMaze({ maze, ctx, scale, width, height, cellWidth, offset });

      drawSolution({
        solution,
        ctx,
        start: graph.getStart(),
        end: graph.getEnd(),
        cellWidth,
      });
    });

    const graph = new Graph({ rows, columns });
    graph.createMaze();

    const maze = graph.getMaze();
    const solution = graph.solveMaze();
  },
};
</script>

<style lang="css">
#maze {
  border: 1px solid black;
  fill: black;
}
</style>