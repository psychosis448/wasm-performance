<template>
  <Suspense>
    <template #default>
      <BenchMark />
    </template>

    <template #fallback>
      <Spinner />
    </template>
  </Suspense>
</template>

<script>
import BenchMark from "@/views/BenchMark";
import Spinner from "@/views/Spinner";

export default {
  name: "Home",
  components: { BenchMark, Spinner },
};
</script>
