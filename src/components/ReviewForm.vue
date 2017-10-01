<template>
  <div class="review-form">
    <div class="review">Fact</div>
    <ul class="options">
      <li v-for="item in options" class="option-wrapper">
        <survey-option :item="item" v-model="selectedOption" name="survey-option" static="true" optionLabel="Commit" :selectedId="selectedId"/>
      </li>
    </ul>
    <div class="reason">
      <div class="choice">User chose {{selectedId}} </div>
      <div v-if="reason" class="reason-content">{{reason}}</div>
      <div v-else class="no-reason-hint">but user did articulate any reason.</div>
    </div>
    <hr/>
    <div class="summary">
      <div>
        <span>A</span>
        <select v-model="betterLabel1">
          <option disabled selected value="0"> -- select -- </option>
          <option value="1">tiny</option>
          <option value="2">small</option>
        </select>
        <select v-model="betterLabel2">
          <option disabled selected value="0"> -- select -- </option>
          <option value="3">feature</option>
          <option value="4">bug fix</option>
          <option value="-1">custom</option>
        </select>
        <span v-if="newLabel1Enabled">(my label: 
        <input v-model="newLabel1" class="new-label" placeholder="new label"  />
        )</span>
      </div>
      <div>is more valuable than</div>
      <div>
        <span>a</span>
        <select v-model="worseLabel1">
          <option disabled selected value="0"> -- select -- </option>
          <option value="1">tiny</option>
          <option value="2">small</option>
        </select>
        <select v-model="worseLabel2">
          <option disabled selected value="0"> -- select -- </option>
          <option value="3">feature</option>
          <option value="4">bug fix</option>
          <option value="-1">custom</option>
        </select>
        <span v-if="newLabel2Enabled" >(my label: 
        <input v-model="newLabel2" class="new-label" placeholder="new label"/>
        )</span>
      </div>
      If no such rule can be derived from the fact, leave a comment:
    </div>
    <div class="buttons">
      <button class="quit-button" v-on:click="quitButtonClicked">Quit</button>
      <button class="save-button" v-on:click="saveButtonClicked" :disabled="!validated">Save & Continue</button>
    </div>
  </div>
</template>

<script>
import Option from '@/components/Option'
export default {
  name: 'ReviewForm',
  components: {
    'survey-option': Option
  },
  computed: {
    selectedId: function () {
      return this.$data.options.reduce(function (a, b) { return a.value > b.value ? a : b }).id
    },
    validated: function () {
      let labels = [this.$data.betterLabel1, this.$data.betterLabel2, this.$data.worseLabel1, this.$data.worseLabel2]
      let scalarValidated = labels.filter(function (x) {
        return parseInt(x) !== 0
      }).length === labels.length
      let contentValidated = true
      if (parseInt(this.$data.betterLabel2) === -1 && this.$data.newLabel1.trim().length === 0) {
        contentValidated = false
      }
      if (parseInt(this.$data.worseLabel2) === -1 && this.$data.newLabel2.trim().length === 0) {
        contentValidated = false
      }
      return scalarValidated && contentValidated
    },
    newLabel1Enabled: function () {
      return parseInt(this.$data.betterLabel2) === -1
    },
    newLabel2Enabled: function () {
      return parseInt(this.$data.worseLabel2) === -1
    }
  },
  data () {
    return {
      reason: '',
      options: [
        {id: 100, text: 'block hotot action', link: 'https://github.com/lyricat/Hotot/commit/50db207cc5', value: 1},
        {id: 101, text: 'new dialog for extensions', link: 'https://github.com/lyricat/Hotot/commit/50db207cc5', value: 0}
      ],
      selectedOption: 0,
      betterLabel1: 0,
      betterLabel2: 0,
      worseLabel1: 0,
      worseLabel2: 0,
      newLabel1: '',
      newLabel2: ''
    }
  },
  methods: {
    saveButtonClicked: function (event) {
      let payload = {
        'labels': [
          [this.$data.betterLabel1, this.$data.betterLabel2 === '-1' ? this.$data.newLabel1 : this.$data.betterLabel2],
          [this.$data.worseLabel1, this.$data.worseLabel2 === '-1' ? this.$data.newLabel2 : this.$data.worseLabel2]
        ]
      }
      console.log('save button clicked, selected option id =', payload)
    },
    quitButtonClicked: function (event) {
      console.log('quit button clicked')
    }
  }
}
</script>

<style scoped>
.review {
  font-size: 20px;
  margin-bottom: 20px;
}
.reason {
  background: #FFFBD0;
  padding: 8px 8px;
  border-radius: 4px;
  border: 1px solid #FFEC9E;
}
.no-reason-hint {
}
.choice {
  font-weight: bold;
}
.summary {
  font-size: 14px;
}
.new-label {
  width: 80px;
}
.options {
  padding: 0;
  margin: 0;
  text-align: left;
  margin-bottom: 10px;
}
.option-wrapper {
  list-style: none;
  border-radius: 4px;
}
.buttons {
  display: flex;
}
.buttons > button {
  margin: 10px;
  flex: 1;
  border: 0;
  border-radius: 4px;
  color: white;
  height: 44px;
  font-weight: bold;
  font-size: 16px;
}
.save-button {
  background: #1DB100;
}
.save-button:disabled {
  opacity: 0.4;
}
.quit-button {
  background: #EE220C;
}
</style>
