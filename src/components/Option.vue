<template>
  <label class="option" v-bind:class="{ selected: selectedId === item.id }"> 
    <input v-if="!static" type="radio" :value="item.id" :name="name"
      v-on:change="updateValue($event)"
    />
    <div v-else class="option-label">
      {{optionLabel}} {{item.id}}
    </div>
    <div class="option-body">
      <div class="option-text">{{ item.text }}</div>
      <div v-if="item.link" ><a class="option-link" :href="item.link">{{item.link}}</a></div>
    </div>
  </label> 
</template>

<script>
export default {
  props: ['item', 'selectedOption', 'name', 'static', 'optionLabel', 'selectedId'],
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
  padding: 4px 8px;
  border-radius: 4px;
}
.option.selected {
  background: #D1FACA;
}
.option:hover {
  background: #f2f2f2;
}
.option.selected:hover {
  background: #D1FACA !important;
}
.option-label {
  font-family: "HelveticaNeue-CondensedBold";
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
