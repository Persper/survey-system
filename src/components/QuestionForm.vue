<template>
  <div class="question-form">
    <div class="question">{{ questionTitle }}</div>
    <ul class="options">
      <li v-for="item in options" class="option-wrapper">
        <survey-option :item="item" v-model="selectedOption" name="survey-option"/>
      </li>
    </ul>
    <div class="reason-label">{{ reasonLabel }}</div>
    <textarea class="reason" placeholder="Write reason here."></textarea>
    <div class="buttons">
      <button class="quit-button" v-on:click="quitButtonClicked">Quit</button>
      <button class="save-button" v-on:click="saveButtonClicked" :disabled="selectedOption === 0">Save & Continue</button>
    </div>
  </div>
</template>

<script>
import Option from '@/components/Option'
export default {
  name: 'QuestionForm',
  components: {
    'survey-option': Option
  },
  data () {
    return {
      questionTitle: 'Which of the following two commits do you think is more valuable to the development of your project?',
      reasonLabel: 'Please explain the above answer (in English or Chinese). Think about both commit-specific reasons and commit-independent factors that may indicate your choice.',
      msg: 'wireframe',
      options: [
        {id: 100, text: 'block hotot action', link: 'https://github.com/lyricat/Hotot/commit/50db207cc5'},
        {id: 101, text: 'new dialog for extensions', link: 'https://github.com/lyricat/Hotot/commit/50db207cc5'},
        {id: -1, text: 'Really not comparable!'},
        {id: -2, text: 'Problematic (e.g., one commit covers too many different changes).'}
      ],
      selectedOption: 0
    }
  },
  methods: {
    saveButtonClicked: function (event) {
      let payload = {
        'selected': this.$data.selectedOption
      }
      console.log('save button clicked, selected option id =', payload)
      this.$http.get('/someUrl').then(response => {
        // success callback
      }, response => {
        // error callback
      })
    },
    quitButtonClicked: function (event) {
      console.log('quit button clicked')
    }
  }
}
</script>

<style scoped>
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
