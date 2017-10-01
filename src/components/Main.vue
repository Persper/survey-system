<template>
  <div class="main">
    <span>Hello. </span>
    <router-link to="/projects/1/questions">Go to questions view</router-link>
  </div>
</template>

<script>
export default {
}
</script>

<style scoped>
a {
  color: #aaf;
}
.main {
  color: white;
  padding-top: 200px;
}
</style>
