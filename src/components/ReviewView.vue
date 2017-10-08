<template>
  <div class="review">
    <wireframe>
      <review-form :review="reviewObject" v-on:result="fetchResult"/>
    </wireframe>
  </div>
</template>

<script>
import Wireframe from '@/components/Wireframe'
import ReviewForm from '@/components/ReviewForm'
import Config from '@/config'
export default {
  name: 'ReviewView',
  components: {
    'wireframe': Wireframe,
    'review-form': ReviewForm
  },
  data () {
    return {
      reviewObject: null
    }
  },
  methods: {
    reload: function () {
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/reviews/next`
      this.$http.get(url).then(function (response) {
        console.log('reload items')
        this.reviewObject = response.body.data.review
      }, function (response) {
        alert('failed to reload, try later.')
      })
    },
    fetchResult: function (result) {
      console.log('result =', result)
      let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/reviews/${this.reviewObject.id}`
      this.$http.post(url, result).then(function (response) {
        this.reload()
      }, function (response) {
        alert('failed to save, try later.')
      })
    }
  },
  created: function () {
    let url = Config.API_BASE + `/projects/${this.$route.params.projectId}/reviews/next`
    this.$http.get(url).then(function (response) {
      console.log('load items', response.body.data.review)
      this.reviewObject = response.body.data.review
    }, function (response) {
      alert('failed to reload, try later.')
    })
  }
}
</script>

<style scoped>
.review {
}
</style>
