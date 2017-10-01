<template>
  <div class="main">
    <wireframe></wireframe>
  </div>
</template>

<script>
import Wireframe from '@/components/Wireframe'
export default {
  name: 'hello',
  components: {
    'wireframe': Wireframe
  },
  data () {
    return {
      msg: 'Main'
    }
  }
}
</script>

<style scoped>

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.main {
}
</style>
