<template>
  <div>
    <h1>WasMaze</h1>
    <canvas id="maze"></canvas>
  </div>
</template>

<script>
import { onMounted } from "vue";
import { drawMaze, drawSolution } from "@/util/canvasDraw";

export default {
  name: "MazeWasm",
  async setup() {
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

      drawMaze({
        maze: wasmMaze,
        ctx,
        scale,
        width,
        height,
        cellWidth,
        offset,
      });

      drawSolution({
        solution,
        ctx,
        start: wasmGraph.get_start(),
        end: wasmGraph.get_end(),
        cellWidth,
      });
    });

    const wasm = await import("../../wasm-pkg/");

    const WasmGraph = wasm.Graph;
    const wasmGraph = new WasmGraph(rows, columns);
    wasmGraph.create_maze();

    const wasmMaze = new Map(Object.entries(wasmGraph.get_maze()));
    const solution = wasmGraph.solve_maze();

    /************js graph -> wasm solve -> solution to js*********************
    // create graph in js
    const jsGraph = new Graph({ rows, columns });
    jsGraph.createMaze();

    // prepare for wasm
    const mazeForWasm = jsGraph.mapForWasm();
    // pass to wasm
    wasmGraph.set_maze_from_js(mazeForWasm);

    // solve :)
    console.log("wasm solution: ", wasmGraph.solve_maze());
    console.log("js solution:", jsGraph.solveMaze());
    *************************************************************************/
  },
};
</script>

<style lang="css">
#maze {
  border: 1px solid black;
  fill: black;
}
</style>