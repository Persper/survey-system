<template>
  <div class="main">
    <h2>Paste your project id and token here</h2>
    <p>
      <input class="project-input" placeholder="project Id here." v-model="project" />
      <input class="token-input" placeholder="token here." v-model="token" />
    </p>
    <p>
      <button class="button" v-on:click="gotoEntryView">Goto Developer Entry</button> <br/>
      or <br/>
      <button class="button" v-on:click="gotoQuestionView">Anwser Questions Directly</button> <br/>
      or <br/>
      <button class="button" v-on:click="gotoReviewVuew">Review Questions</button> <br/>
    </p>
  </div>
</template>

<script>
import Vue from 'vue'
import Storage from '@/mixins/storage'
export default {
  mixins: [Storage],
  data () {
    return {
      token: '',
      project: ''
    }
  },
  methods: {
    gotoEntryView: function (evt) {
      this.saveToken(this.token)
      Vue.http.headers.common['X-USR-TOKEN'] = this.token
      this.$router.push({name: 'Entry', params: {token: this.token}, query: {projectId: this.project}})
      return
    },
    gotoQuestionView: function (evt) {
      this.saveToken(this.token)
      Vue.http.headers.common['X-USR-TOKEN'] = this.token
      this.$router.push({name: 'QuestionView', params: {projectId: this.project}})
      return
    },
    gotoReviewVuew: function (evt) {
      this.saveToken(this.token)
      Vue.http.headers.common['X-USR-TOKEN'] = this.token
      this.$router.push({name: 'ReviewView', params: {projectId: this.project}})
    }
  }

}
</script>

<style scoped>
a {
  color: #aaf;
}
.project-input, .token-input {
  width: 400px;
  height: 30px;
  font-size: 18px;
}
.button {
  height: 30px;
}
.main {
  width: 600px;
  margin: 0 auto;
  color: white;
  padding-top: 200px;
  text-align: left;
}
</style>
