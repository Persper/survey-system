<template>
  <div class="wireframe">
    <slot>
      Something went wrong!
    </slot>
    <div v-if="isLoading" class="loader-mask">
      <div class="loader-wrapper">
        <loader class="loader"></loader>
      </div>
    </div>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'

export default {
  components: {
    'loader': ScaleLoader
  },
  props: ['isLoading']
}
</script>

<style scoped>
.wireframe {
  border-radius: 2px;
  background: white;
  width: 600px;
  min-height: 400px;
  margin: 40px auto 0 auto;
  line-height: 1.4;
  font-size: 16px;
  padding: 20px 40px;
  text-align: left;
  position: relative;
}
.loader-mask {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0,0,0,0.1);
  z-index: 99;
}
.loader-wrapper {
  background: rgba(255,255,255,1);
  box-shadow: 0 0 20px rgba(0,0,0,0.2);
  border-radius: 4px;
  padding: 20px 0;
  position: absolute;
  top: 50%;
  left: 50%;
  width: 120px;
  height: 40px;
  margin-left: -60px;
  margin-top: -50px;
  z-index: 100;
}
</style>
