<template>
  <div class="question">
    <wireframe :isLoading="isLoading">
      <div v-if="isCompleted">
        {{completedHint}}
      </div>
      <question-form v-else :question="questionObject" :progress="progress" :count="count" v-on:result="fetchResult" v-on:back="back"/>
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
      isLoading: false,
      progress: {
        answered: 0
      }
    }
  },
  methods: {
    reload: function () {
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/questions/next`
      this.$http.get(url).then(function (response) {
        console.log('reload items')
        if (response.body.status !== 0) {
          this.isCompleted = true
          this.completedHint = response.body.message
        } else {
          this.questionObject = response.body.data.question
          this.progress.answered = response.body.data.question.answered + 1
        }
        this.isLoading = false
        this.count += 1
      }, function (response) {
        alert('Failed to reload. Please try later.')
      })
    },
    fetchResult: function (result) {
      this.isLoading = true
      console.log('result =', result)
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/questions/${this.questionObject.id}`
      // prepared, send data
      this.$http.post(url, result).then(function (response) {
        this.reload()
      }, function (response) {
        alert('Failed to save. Please try later.')
      })
    },
    back: function () {
      this.$router.push({name: 'Entry', params: {token: this.token}, query: {projectId: this.$route.params.projectId}})
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
