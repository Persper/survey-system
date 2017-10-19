<template>
  <div class="question">
    <wireframe>
      <div v-if="isCompleted">
        {{completedHint}}
      </div>
      <question-form v-else :question="questionObject" :count="count" v-on:result="fetchResult"/>
    </wireframe>
    <div v-if="isLoading" class="loader-mask">
      <div class="loader-wrapper">
        <loader class="loader"></loader>
      </div>
    </div>
  </div>
</template>

<script>
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'
import Wireframe from '@/components/Wireframe'
import QuestionForm from '@/components/QuestionForm'
import Storage from '@/mixins/storage'
import Config from '@/config'

export default {
  name: 'QuestionView',
  mixins: [Storage],
  components: {
    'loader': ScaleLoader,
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

.loader-mask {
  position: fixed;
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
  margin-top: 50px;
  z-index: 100;
}
</style>
