<template>
  <div class="main">
    <h2>Hello. Paste your token here and click the link below</h2>
    <p>
      <input class="token-input" placeholder="token here." v-model="token" />
      <button class="token-button" v-on:click="tokenButtonClick">Use this token</button>
    </p>
    <ul>
      <li>
        <router-link to="/projects/de65f79e6f3391866ab4d68cbebeee1bcdc859f0/questions">Go to questions view</router-link>,
      </li>
      <li>
        <router-link to="/projects/de65f79e6f3391866ab4d68cbebeee1bcdc859f0/reviews">Go to review view</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import Vue from 'vue'
import Storage from '@/mixins/storage'
export default {
  mixins: [Storage],
  data () {
    return {
      // token: 'eA-eVprwiID0FlOfTpkFIP8BRIMz1VmLaNs6r-6Aq34'
      token: '-sByKwtRLkb9O6nsYhs29j-muE4pT-TwLcYyC3HJSPY'
    }
  },
  methods: {
    tokenButtonClick: function (evt) {
      this.saveToken(this.token)
      Vue.http.headers.common['X-USR-TOKEN'] = this.token
      return
    }
  }

}
</script>

<style scoped>
a {
  color: #aaf;
}
.token-input {
  width: 400px;
  height: 30px;
  font-size: 18px;
}
.token-button {
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
