<template>
</template>

<script>
import Vue from 'vue'
import Storage from '@/mixins/storage'

export default {
  name: 'Entry',
  mixins: [Storage],
  components: {
  },
  data () {
    return {
    }
  },
  methods: {
  },
  created: function () {
    let token = this.$route.params.token
    console.log(token)
    let projectId = this.$route.query.project
    this.saveToken(token)
    Vue.http.headers.common['X-USR-TOKEN'] = token
    this.$router.push({name: 'QuestionView', params: {projectId: projectId}})
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
