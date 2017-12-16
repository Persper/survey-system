<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
html, body {
  margin: 0;
}
body {
  background: #333;
}
#app {
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
textarea, input[type="text"] {
  font-size: 14px;
}
.button {
  flex: 1;
  border: 0;
  border-radius: 4px;
  color: white;
  height: 44px;
  font-weight: bold;
  font-size: 16px;
  background: #1DB100;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 auto;
}

th {
  font-weight: bold;
  border: 1px solid #ccc;
}

th.sub {
  background-color: #f2f2f2 !important;
}

td {
  text-align: left;
  padding: 3px 10px 2px;
  border-bottom: 1px solid #ccc;
}
</style>
