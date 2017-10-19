import Vue from 'vue'
export default {
  data () {
    return {
      token: null
    }
  },
  methods: {
    loadToken () {
      let token = this.token
      if (token === null) {
        token = window.localStorage.getItem('token')
        Vue.http.headers.common['X-USR-TOKEN'] = token
        this.token = token
      }
      return token
    },
    saveToken (token) {
      this.token = token
      window.localStorage.setItem('token', token)
    }
  }
}
