<template>
  <div class="wireframe">
    <div class="question">{{ questionTitle }}</div>
    <ul class="options">
      <li v-for="item in options" class="option">
        <label class="option-inner"> 
          <input type="radio" v-model="selectedOption" :value="item.id"/>
          <div class="option-body">
            <div class="option-text">{{ item.text }}</div>
            <div v-if="item.link" ><a class="option-link" :href="item.link">{{item.link}}</a></div>
          </div>
        </label> 
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
export default {
  name: 'hello',
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
    },
    quitButtonClicked: function (event) {
      console.log('quit button clicked')
    }
  }
}
</script>

<style scoped>
.wireframe {
  border-radius: 2px;
  background: white;
  width: 600px;
  height: 500px;
  margin: 40px auto 0 auto;
  line-height: 1.4;
  font-size: 16px;
  padding: 20px 40px;
  text-align: left;
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
.option {
  list-style: none;
  padding: 4px 8px;
  border-radius: 4px;
}
.option:hover {
  background: #f2f2f2;
}
.option-inner {
  display: flex;
  height: 44px;
}
.option-body {
  margin-left: 10px;
}
.option-link {
  color: #888;
  font-size: 14px;
  padding: 4px 0;
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
