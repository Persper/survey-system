<template>
  <div class="main">
    <wireframe>
    <div class="container">
      <div class="title">
        You are invited to take a survey.
      </div>
      <div class="project-info">
        <div class="project-name">Hotot</div>
        <div class="project-info-body">
          <div class="rows">
            <div class="row">
              <div class="label">Persper Repo</div>
              <div class="value"><a href="https://persper.org/{%project_name%}">https://persper.org/{%project_name%}</a></div>
            </div>
            <div class="row">
              <div class="label">Persper Index</div>
              <div class="value">{%index%}</div>
            </div>
            <div class="row">
              <div class="label">Commits</div>
              <div class="value">{%count%}</div>
            </div>
            <div class="row">
              <div class="label">Github Repo</div>
              <div class="value"><a href="https://persper.org/{%project_name%}">https://github.com/{%project_name%}</a></div>
            </div>
          </div>
          <div class="explanation">
            <div class="explanation-content">
              Here we need to introduce what's persper repo and our decentralized git system. blah blah 
              <a href="">Learn more</a>
            </div>
          </div>
        </div>
      </div>
      <div class="survey-info">
        <p>
          Your have completed {%count%} questions and {%count%} have been reviewed. Next, we'll provide {%count%} questions.
        </p>
        <p class="left">
          <button class="button" v-on:click="gotoQuestionView">Anwser Questions</button>
        </p>
      </div>
      <div class="hint">
        We collect data about the use of commit-related information by every project in Persper. These data provide opportunities to understand and improve Persper's evaluate system. blah blah bluh bluh...
      </div>
    </div>
  </wireframe>
  </div>
</template>

<script>
import Vue from 'vue'
import Wireframe from '@/components/Wireframe'
import Storage from '@/mixins/storage'

export default {
  name: 'Entry',
  mixins: [Storage],
  components: {
    'wireframe': Wireframe
  },
  data () {
    return {
    }
  },
  methods: {
    gotoQuestionView: function (evt) {
      let projectId = this.$route.query.project
      this.$router.push({name: 'QuestionView', params: {projectId: projectId}})
    }
  },
  created: function () {
    let token = this.$route.params.token
    // console.log(token)
    // save and set token
    this.saveToken(token)
    Vue.http.headers.common['X-USR-TOKEN'] = token
  }
}
</script>

<style scoped>
.container {
  padding: 0;
}
.title, .project-info, .survey-info {
  border-bottom: 1px solid #eee;
  padding: 20px 0;
  font-size: 14px;
}
.project-name {
  font-size: 20px;
  padding: 0;
  margin-bottom: 10px;
}
.project-info-body {
  display: flex;
  flex-direction: row;
}
.project-info .row {
  margin-bottom: 4px;
}
.project-info .label {
  font-size: 10px;
}
.project-info .value {
  font-family: monospace;
}
.project-info .explanation-content {
  margin-left: 20px;
  border-radius: 4px;
  border: 1px solid #f2f2f2;
  padding: 20px;
  background: #f2f2f2;
  position: relative;
}
.project-info .explanation-content::after {
  position: absolute;
  height: 0;
  width: 0;
  border-width: 10px;
  border-color: transparent #f2f2f2 transparent transparent;
  border-style: solid;
  display: block;
  content: ' ';
  left: 0;
  top: 12px;
  margin-left: -20px;
}
.survey-info {
  display: flex;
  flex-direction: row;
}
.survey-info > p {
  margin: 0;
}
.survey-info .button {
  width: 180px;
  font-size: 14px;
}
.hint {
  margin-top: 20px;
  background: rgba(255, 255, 0, 0.4);
  border-radius: 2px;
  border: 1px solid rgba(255, 200, 0, 0.4);
  padding: 10px;
  font-size: 12px;
}
</style>
