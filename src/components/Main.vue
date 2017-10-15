<template>
  <div class="main">
    <span>Hello. </span>
    <ul>
      <li>
        <router-link to="/projects/e9ec2d029eaf66bb03a6e426649d69018be7633a/questions">Go to questions view</router-link>,
      </li>
      <li>
        <router-link to="/projects/e9ec2d029eaf66bb03a6e426649d69018be7633a/reviews">Go to review view</router-link>
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
