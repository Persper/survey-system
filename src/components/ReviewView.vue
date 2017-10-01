<template>
  <div class="review">
    <wireframe>
      <review-form/>
    </wireframe>
  </div>
</template>

<script>
import Wireframe from '@/components/Wireframe'
import ReviewForm from '@/components/ReviewForm'
export default {
  name: 'hello',
  components: {
    'wireframe': Wireframe,
    'review-form': ReviewForm
  },
  data () {
    return {
      msg: 'Main'
    }
  }
}
</script>

<style scoped>
.review {
}
</style>
