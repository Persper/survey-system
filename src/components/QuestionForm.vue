<template>
  <div class="question-form">
    <div v-if="question">
      <div class="question">{{ questionTitle }}</div>
      <ul class="options">
        <li v-for="item in options" class="option-wrapper">
          <survey-option :item="item" v-model="selectedOption" name="survey-option"></survey-option>
        </li>
      </ul>
      <div class="reason-label">{{ reasonLabel }}</div>
      <textarea class="reason" placeholder="Write reason here." v-model="comment"></textarea>
      <div class="buttons">
        <button class="quit-button" v-on:click="quitButtonClicked">Quit</button>
        <button class="save-button" v-on:click="saveButtonClicked" :disabled="selectedOption === 0 || comment.trim().length === 0">Save & Continue</button>
      </div>
    </div>
  </div>
</template>

<script>
import Option from '@/components/Option'
// import Config from '@/config'
export default {
  name: 'QuestionForm',
  components: {
    'survey-option': Option
  },
  props: ['question', 'count'],
  data () {
    return {
      questionTitle: 'Which of the following two commits do you think is more valuable to the development of your project?',
      reasonLabel: 'Please explain the above answer. Think about both commit-specific reasons and commit-independent factors that may indicate your choice.',
      selectedOption: 0,
      comment: ''
    }
  },
  computed: {
    options: function () {
      if (this.question) {
        let ret = this.question.commits.map(function (x) {
          return {
            id: x.id, text: x.title, link: x.url
          }
        })
        ret = ret.concat([
          {id: -1, text: 'Really not comparable!'},
          {id: -2, text: 'Problematic (e.g., one commit covers too many different changes).'}
        ])
        return ret
      }
      return []
    }
  },
  watch: {
    count: function (a, b) {
      this.selectedOption = 0
      this.comment = ''
      console.log('reset form', this.selectedOption)
    }
  },
  methods: {
    saveButtonClicked: function (event) {
      let payload = {
        'selected': this.selectedOption,
        'reason': this.comment
      }
      this.$emit('result', payload)
    },
    quitButtonClicked: function (event) {
      alert('close the window and leave.')
    }
  }
}
</script>

<style scoped>
.loader {
  margin: 10px auto;
  text-align: center;
}
.question {
  font-size: 20px;
  margin-bottom: 20px;
}
.reason-label {
  margin-bottom: 8px;
}
.reason {
  display: block;
  width: 100%;
  border: #888 1px solid;
  height: 100px;
}
.options {
  padding: 0;
  margin: 0;
  text-align: left;
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
