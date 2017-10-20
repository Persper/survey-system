<template>
  <div class="question">
    <wireframe :isLoading="isLoading">
      <div v-if="isCompleted">
        {{completedHint}}
      </div>
      <question-form v-else :question="questionObject" :count="count" v-on:result="fetchResult"/>
    </wireframe>
  </div>
</template>

<script>
import Wireframe from '@/components/Wireframe'
import QuestionForm from '@/components/QuestionForm'
import Storage from '@/mixins/storage'
import Config from '@/config'

export default {
  name: 'QuestionView',
  mixins: [Storage],
  components: {
    'wireframe': Wireframe,
    'question-form': QuestionForm
  },
  data () {
    return {
      count: 0,
      questionObject: null,
      isCompleted: false,
      completedHint: '...',
      isLoading: false
    }
  },
  methods: {
    reload: function () {
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/questions/next`
      this.$http.get(url).then(function (response) {
        console.log('reload items')
        if (response.body.status === 100) {
          this.isCompleted = true
          this.completedHint = response.body.message
        } else {
          this.questionObject = response.body.data.question
        }
        this.isLoading = false
        this.count += 1
      }, function (response) {
        alert('failed to reload, try later.')
      })
    },
    fetchResult: function (result) {
      this.isLoading = true
      console.log('result =', result)
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/questions/${this.questionObject.id}`
      // prepared, send data
      this.$http.post(url, result).then(function (response) {
        this.reload()
        this.count += 1
      }, function (response) {
        alert('failed to save, try later.')
      })
    }
  },
  created: function () {
    this.isLoading = true
    this.loadToken()
    this.reload()
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

</style>
