<template>
  <Suspense>
    <template #default>
      <MazeJs v-if="mazeJs" />
      <MazeWasm v-else />
    </template>

    <template #fallback>
      <Spinner />
    </template>
  </Suspense>
</template>

<script>
import MazeJs from "@/views/MazeJs";
import MazeWasm from "@/views/MazeWasm";
import Spinner from "@/views/Spinner";

export default {
  name: "Maze",
  components: { Spinner, MazeJs, MazeWasm },
  computed: {
    mazeJs() {
      return this.$route.path.includes("js");
    },
  },
};
</script>
