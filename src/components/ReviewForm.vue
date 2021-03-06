<template>
  <div v-if="review">
    <div class="review-form">
      <div class="review">Fact</div>
      <ul class="options">
        <li v-for="item in options" class="option-wrapper">
          <survey-option :item="item" v-model="selectedOption" name="survey-option" static="true" optionLabel="Commit" :selectedId="selectedId"/>
        </li>
      </ul>
      <div class="reason">
        <div class="choice">User chose {{selectedId}} </div>
        <div v-if="review.reason" class="reason-content">{{review.reason}}</div>
        <div v-else class="no-reason-hint">but user did articulate any reason.</div>
      </div>
      <hr/>
      <div class="summary">
        <p>
        <span>
          <span>A</span>
          <select v-model="betterLabel1">
            <option disabled selected value="0"> -- select -- </option>
            <option v-for="label in labels.builtin" :value="label.id">{{label.name}}</option>
          </select>
          <select v-model="betterLabel2">
            <option disabled selected value="0"> -- select -- </option>
            <option v-for="label in labels.customized" :value="label.id">{{label.name}}</option>
            <option value="-1">custom</option>
          </select>
          <span v-if="newLabel1Enabled">
            <input v-model="newLabel1" class="new-label" placeholder="new label"  />
          </span>
        </span>
        <span>is more valuable than</span>
        <span>
          <span>a</span>
          <select v-model="worseLabel1">
            <option disabled selected value="0"> -- select -- </option>
            <option v-for="label in labels.builtin" :value="label.id">{{label.name}}</option>
          </select>
          <select v-model="worseLabel2">
            <option disabled selected value="0"> -- select -- </option>
            <option v-for="label in labels.customized" :value="label.id">{{label.name}}</option>
            <option value="-1">custom</option>
          </select>
          <span v-if="newLabel2Enabled" >
            <input v-model="newLabel2" class="new-label" placeholder="new label"/>
          </span>
        </span>
        </p>
        <div>If no such rule can be derived from the fact, leave a comment:</div>
        <textarea v-model="comment" class="comment-area"></textarea>
      </div>
      <div class="buttons">
        <button class="quit-button" v-on:click="quitButtonClicked">Quit</button>
        <button class="save-button" v-on:click="saveButtonClicked" :disabled="!validated">Save & Continue</button>
      </div>
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
  props: ['review', 'labels', 'count'],
  computed: {
    selectedId: function () {
      return this.review.selected
    },
    notSelectedId: function () {
      for (var i = 0; i < this.review.commits.length; i += 1) {
        if (this.review.selected !== this.review.commits[i].id) {
          return this.review.commits[i].id
        }
      }
      return 0
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
      let reasonValidated = true
      if (this.$data.comment.trim().length === 0) {
        reasonValidated = false
      }
      return reasonValidated || (scalarValidated && contentValidated)
    },
    newLabel1Enabled: function () {
      return parseInt(this.$data.betterLabel2) === -1
    },
    newLabel2Enabled: function () {
      return parseInt(this.$data.worseLabel2) === -1
    },
    options: function () {
      if (this.review) {
        let ret = this.review.commits.map(function (x) {
          return {
            id: x.id, text: x.title, link: x.url, displayedId: x.id.substring(0, 10)
          }
        })
        // ret = ret.concat([
        //   {id: -1, text: 'Really not comparable!'},
        //   {id: -2, text: 'Problematic (e.g., one commit covers too many different changes).'}
        // ])
        return ret
      }
      return []
    }
  },
  watch: {
    count: function (a, b) {
      this.$data.selectedOption = 0
      this.$data.betterLabel1 = 0
      this.$data.betterLabel2 = 0
      this.$data.worseLabel1 = 0
      this.$data.worseLabel2 = 0
      this.$data.newLabel1 = ''
      this.$data.newLabel2 = ''
      this.$data.comment = ''
    }
  },
  data () {
    return {
      reason: '',
      selectedOption: 0,
      betterLabel1: 0,
      betterLabel2: 0,
      worseLabel1: 0,
      worseLabel2: 0,
      newLabel1: '',
      newLabel2: '',
      comment: ''
    }
  },
  methods: {
    saveButtonClicked: function (event) {
      let payload = {
        'commitLabels': [
          {labelId: this.$data.betterLabel1, commitId: this.selectedId},
          {labelId: this.$data.betterLabel2, commitId: this.selectedId},
          {labelId: this.$data.worseLabel1, commitId: this.notSelectedId},
          {labelId: this.$data.worseLabel2, commitId: this.notSelectedId}
        ],
        'comment': this.$data.comment
      }
      if (this.$data.betterLabel2 === '-1') {
        payload['commitLabels'][1].labelName = this.$data.newLabel1
        delete payload['commitLabels'][1].labelId
      }
      if (this.$data.worseLabel2 === '-1') {
        payload['commitLabels'][3].labelName = this.$data.newLabel2
        delete payload['commitLabels'][3].labelId
      }
      console.log('save button clicked, selected option id =', payload)
      this.$emit('result', payload)
    },
    quitButtonClicked: function (event) {
      this.$emit('back', {})
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
.comment-area {
  width: 100%;
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
