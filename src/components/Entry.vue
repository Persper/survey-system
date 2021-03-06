<template>
  <div class="main">
    <wireframe>
    <div class="container">
      <div class="title">
        Welcome to the Persper Foundation Code Value survey!
        <div class="guideline">
          <p>Thank you for participating in this survey for evaluating code contributions. The survey result will help innovate the recognizing and rewarding mechanisms for open source developers and may lead to more sustainable open source development.
          </p>
          <p>
          You will compare pairs of commits of the following project that you have contributed to.
          </p>
        </div>
      </div>
      <div class="project-info">
        <div class="project-name">{{ projectName }}</div>
        <div class="project-info-body">
          <div class="rows">
            <div class="row">
              <div class="label">Github Repo</div>
              <div class="value"><a :href="githubUrl">{{githubUrl}}</a></div>
            </div>
          </div>
        </div>
      </div>
      <div class="survey-info">
        <p>
          You have compared <b>{{answered}}</b> out of <b>{{total}}</b> pairs of commits. Please feel free to stop and resume anytime.
        </p>
        <p class="left">
          <button class="button" v-on:click="gotoQuestionView">Answer Questions</button>
        </p>
      </div>
      <div class="hint">
        If you have any questions or suggestions, please email us: <a href="mailto:survey@persper.org">survey@persper.org</a>
      </div>
    </div>
  </wireframe>
  </div>
</template>

<script>
import Vue from 'vue'
import Wireframe from '@/components/Wireframe'
import Storage from '@/mixins/storage'
import Config from '@/config'

export default {
  name: 'Entry',
  mixins: [Storage],
  components: {
    'wireframe': Wireframe
  },
  data () {
    return {
      isCompleted: false,
      completedHint: '...',
      total: 0,
      answered: 0,
      githubUrl: 'loading...',
      projectName: '',
      projectId: ''
    }
  },
  methods: {
    gotoQuestionView: function (evt) {
      let projectId = this.$route.query.projectId
      this.$router.push({name: 'QuestionView', params: {projectId: projectId}})
    }
  },
  created: function () {
    let token = this.$route.params.token
    // console.log(token)
    // save and set token
    this.saveToken(token)
    Vue.http.headers.common['X-USR-TOKEN'] = token
    // get developer status
    let url = Config.API_BASE + `/projects/${this.$route.query.projectId}/developer-stats`
    this.$http.get(url).then(function (response) {
      if (response.body.status !== 0) {
        this.isCompleted = true
        this.completedHint = response.body.message
      } else {
        this.answered = response.body.data.answered
        this.total = response.body.data.total
      }
    }, function (response) {
      alert('Failed to load. Please close and reopen.')
    })

    url = Config.API_BASE + `/projects/${this.$route.query.projectId}/project-info`
    this.$http.get(url).then(function (response) {
      if (response.body.status === 0) {
        this.githubUrl = response.body.data.project.githubUrl
        this.projectName = response.body.data.project.name
        this.projectId = response.body.data.project.id
      }
    }, function (response) {
      alert('Failed to load. Please close and reopen.')
    })
  }
}
</script>

<style scoped>
.container {
  padding: 0;
}
.title, .project-info, .survey-info {
  border-bottom: 1px solid #eee;
  padding: 16px 0;
  font-size: 14px;
}
.title {
  font-weight: bold;
  padding-bottom: 0;
}
.guideline {
  font-size: 14px;
  font-weight: normal;
  padding-top: 10px;
  opacity: 0.6;
}
.guideline p {
  margin: 0 0 8px 0;
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
  font-size: 14px;
}
.project-info .value {
  font-family: monospace;
}
.project-info .explanation {
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
  /*display: flex;*/
  /*flex-direction: row;*/
}
.survey-info > p {
  margin: 0;
}
.survey-info .button {
  width: 180px;
  font-size: 14px;
  margin-left: 10px;
  margin: 20px auto 10px auto;
  display: block;
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
