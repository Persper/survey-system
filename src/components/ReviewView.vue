<template>
  <div class="review">
    <wireframe :isLoading="isLoading">
      <div v-if="isCompleted">
        {{completedHint}}
      </div>
      <review-form v-else :review="reviewObject" :labels="labels" :count="count" v-on:result="fetchResult" v-on:back="back"/>
    </wireframe>
  </div>
</template>

<script>
import Wireframe from '@/components/Wireframe'
import ReviewForm from '@/components/ReviewForm'
import Storage from '@/mixins/storage'
import Config from '@/config'

export default {
  name: 'ReviewView',
  mixins: [Storage],
  components: {
    'wireframe': Wireframe,
    'review-form': ReviewForm
  },
  data () {
    return {
      isCompleted: false,
      completedHint: '...',
      isLoading: false,
      count: 0,
      reviewObject: null,
      labels: {
        builtin: [],
        customized: []
      }
    }
  },
  methods: {
    reload: function () {
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/reviews/next`
      this.$http.get(url).then(function (response) {
        // @TODO need to refactor, request and response handling should move to requests mixin
        if (response.body.status !== 0) {
          this.isCompleted = true
          this.completedHint = response.body.message
        } else {
          this.reviewObject = response.body.data.review
        }
        this.count += 1
        this.isLoading = false
      }, function (response) {
        alert('Failed to reload. Please try later.')
      })
    },
    fetchResult: function (result) {
      this.isLoading = true
      console.log('result =', result)
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/reviews/${this.reviewObject.id}`
      this.$http.post(url, result).then(function (response) {
        this.loadLabels()
        this.reload()
      }, function (response) {
        alert('Failed to save. Please try later.')
      })
    },
    loadLabels: function () {
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/labels`
      this.$http.get(url).then(function (response) {
        console.log('reload labels', response.body.data)
        this.labels = response.body.data
      }, function (response) {
        alert('Failed to reload. Please try later.')
      })
    },
    back: function () {
      this.$router.push({name: 'Entry', params: {token: this.token}, query: {projectId: this.$route.params.projectId}})
    }
  },
  created: function () {
    this.isLoading = true
    this.loadToken()
    this.loadLabels()
    this.reload()
    // let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/reviews/next`
    // this.$http.get(url).then(function (response) {
    //   console.log('load items', response.body.data.review)
    //   this.reviewObject = response.body.data.review
    // }, function (response) {
    //   alert('Failed to load. Please try later.')
    // })
  }
}
</script>

<style scoped>
.review {
}
</style>
