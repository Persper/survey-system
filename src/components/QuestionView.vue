<template>
  <div class="question">
    <wireframe>
      <question-form :question="questionObject" v-on:result="fetchResult"/>
    </wireframe>
  </div>
</template>

<script>
import Wireframe from '@/components/Wireframe'
import QuestionForm from '@/components/QuestionForm'
import Config from '@/config'
export default {
  name: 'QuestionView',
  components: {
    'wireframe': Wireframe,
    'question-form': QuestionForm
  },
  data () {
    return {
      questionObject: null
    }
  },
  methods: {
    reload: function () {
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/questions/next`
      this.$http.get(url).then(function (response) {
        console.log('reload items')
        this.questionObject = response.body.data.question
      }, function (response) {
        alert('failed to reload, try later.')
      })
    },
    fetchResult: function (result) {
      console.log('result =', result)
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/questions/${this.questionObject.id}`
      // prepared, send data
      this.$http.post(url, result).then(function (response) {
        this.reload()
      }, function (response) {
        alert('failed to save, try later.')
      })
    }
  },
  created: function () {
    let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/questions/next`
    this.$http.get(url).then(function (response) {
      console.log('load items', response.body.data.question)
      this.questionObject = response.body.data.question
    }, function (response) {
      alert('failed to reload, try later.')
    })
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
