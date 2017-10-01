<template>
  <label class="option"> 
    <input type="radio" :value="item.id" :name="name"
      v-on:change="updateValue($event)"
    />
    <div class="option-body">
      <div class="option-text">{{ item.text }}</div>
      <div v-if="item.link" ><a class="option-link" :href="item.link">{{item.link}}</a></div>
    </div>
  </label> 
</template>

<script>
export default {
  props: ['item', 'selectedOption', 'name'],
  data () {
    return {
      selected: this.selectedOption
    }
  },
  methods: {
    updateValue: function (event) {
      this.$emit('input', event.target.value)
    }
  }
}
</script>

<style scoped>
.option {
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
</style>
