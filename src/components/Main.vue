<template>
  <div class="main">
    <span>Hello. </span>
    <ul>
      <li>
        <router-link to="/projects/6f2295863057c2e7059b74a01c79ab707f8789c3/questions">Go to questions view</router-link>,
      </li>
      <li>
        <router-link to="/projects/6f2295863057c2e7059b74a01c79ab707f8789c3/reviews">Go to review view</router-link>
      </li>
    </ul>
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
  width: 600px;
  margin: 0 auto;
  color: white;
  padding-top: 200px;
  text-align: left;
}
</style>
