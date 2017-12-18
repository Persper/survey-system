<template>
  <div class="question-form">
    <div v-if="question">
      <div class="progress">#{{ progress.answered }} Question</div>
      <div class="question">{{ questionTitle }}</div>
      <ul class="options">
        <li v-for="item in options" class="option-wrapper">
          <survey-option :item="item" v-model="selectedOption" name="survey-option"></survey-option>
        </li>
      </ul>
      <div class="reason-label">{{ reasonLabel }}</div>
      <div>
        <div class="commit-comment">
          <span>Commit <code>{{shortHash(question.commits[0].id)}}</code> does/is/has </span>
          <input type="text" v-model="commitCommentA"/>
        </div>
        <div class="commit-comment">
          <span>Commit <code>{{shortHash(question.commits[1].id)}}</code> does/is/has </span>
          <input type="text" v-model="commitCommentB"/>
        </div>
        <div class="commit-comment">
          <span v-if="selectedOption.constructor === String && selectedOption.length > 3">
          Therefore, Commit <code>{{shortHash(selectedOption)}}</code> is more valuable than Commit <code>{{shortHash(notSelected.id)}}
          </code></span>
        </div>
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
// import Config from '@/config'
export default {
  name: 'QuestionForm',
  components: {
    'survey-option': Option
  },
  props: ['question', 'progress', 'count'],
  data () {
    return {
      questionTitle: 'Which of the following two commits do you think is more valuable to the development of your project?',
      reasonLabel: 'Please explain the above answer. Think about both commit-specific reasons and commit-independent factors that may indicate your choice.',
      selectedOption: 0,
      commitCommentA: '',
      commitCommentB: '',
      comment: ''
    }
  },
  computed: {
    options: function () {
      let _this = this
      if (this.question) {
        let ret = this.question.commits.map(function (x) {
          return {
            id: x.id,
            text: 'Commit ' + _this.shortHash(x.id) + ': ' + x.title,
            link: x.url
          }
        })
        ret = ret.concat([
          {id: -1, text: 'Really not comparable!'},
          {id: -2, text: 'Problematic (e.g., one commit covers too many different changes).'}
        ])
        return ret
      }
      return []
    },
    notSelected: function () {
      for (var i = 0; i < this.question.commits.length; i += 1) {
        if (this.selectedOption !== this.question.commits[i].id) {
          return this.question.commits[i]
        }
      }
      return 0
    },
    validated: function () {
      let opt = String(this.selectedOption)
      if (opt === '-1' || opt === '-2') {
        return true
      }
      return opt !== '0' && this.commitCommentA.trim().length !== 0 && this.commitCommentB.trim().length !== 0
    }
  },
  watch: {
    count: function (a, b) {
      this.selectedOption = 0
      this.commitCommentA = ''
      this.commitCommentB = ''
      this.commitCommentA = this.question.commits[0].description || ''
      this.commitCommentB = this.question.commits[1].description || ''
      console.log('reset form', this.selectedOption)
    }
  },
  methods: {
    shortHash: function (hash) {
      return hash.substring(0, 7)
    },
    saveButtonClicked: function (event) {
      var reason = ''
      if (this.selectedOption === this.question.commits[0].id) {
        reason = `[${this.commitCommentA}] is more valuable than [${this.commitCommentB}]`
      } else if (this.selectedOption === this.question.commits[1].id) {
        reason = `[${this.commitCommentB}] is more valuable than [${this.commitCommentA}]`
      }
      let payload = {
        'selected': this.selectedOption,
        'reason': reason
      }
      console.log(payload)
      this.$emit('result', payload)
    },
    quitButtonClicked: function (event) {
      this.$emit('back', {})
    }
  }
}
</script>

<style scoped>
.loader {
  margin: 10px auto;
  text-align: center;
}
.progress {
  color: blue;
  margin: 4px 0;
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
.commit-comment {
  display: flex;
  margin-bottom: 10px;
}
.commit-comment input {
  flex: 1;
  margin-left: 10px;
}
code {
  color: #1DB100;
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
  background: #666;
}
</style>
