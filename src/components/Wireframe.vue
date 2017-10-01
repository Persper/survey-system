<template>
  <div class="wireframe">
    <slot>
      Something went wrong!
    </slot>
  </div>
</template>

<script>
export default {
}
</script>

<style scoped>
.wireframe {
  border-radius: 2px;
  background: white;
  width: 600px;
  height: 500px;
  margin: 40px auto 0 auto;
  line-height: 1.4;
  font-size: 16px;
  padding: 20px 40px;
  text-align: left;
}
</style>
