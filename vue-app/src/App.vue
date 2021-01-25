<template>
  <div>
    <h1>JavaScript vs WebAssembly</h1>
    <router-view v-if="webAssemblySupport && webWorkerSupport"></router-view>
    <div v-else>
      <p>This page requires WebWorkers and WebAssembly.</p>
      <p>Your browser supports:</p>
      <ul>
        <li>WebWorker: {{ webWorkerSupport }}</li>
        <li>WebAssembly: {{ webAssemblySupport }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  setup() {
    const webWorkerSupport = typeof Worker !== undefined;

    const webAssemblySupport =
      typeof WebAssembly === "object" &&
      typeof WebAssembly.instantiate === "function";

    return {
      webWorkerSupport,
      webAssemblySupport,
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
