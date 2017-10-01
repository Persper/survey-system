<template>
  <div class="question">
    <wireframe>
      <question-form/>
    </wireframe>
  </div>
</template>

<script>
import Wireframe from '@/components/Wireframe'
import QuestionForm from '@/components/QuestionForm'
export default {
  name: 'hello',
  components: {
    'wireframe': Wireframe,
    'question-form': QuestionForm
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

.question {
}
</style>
