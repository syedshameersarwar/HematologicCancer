<template>
  <div id="app">
    <img id="ned" alt="Vue logo" src="./assets/logo.png" />
    <HelloWorld msg="Early Screening and Detection of Hematologic Cancer using Complete Blood Count"/>
    <UploadCSV/>
  </div>
</template>

<script>
import HelloWorld from "./components/Header/HelloWorld.vue";
import UploadCSV from "./components/uploadCSV/uploadCSV.vue";

export default {
  name: "App",
  components: {
    HelloWorld,
    UploadCSV,
  }, 
  data: () =>{
    return {

    };
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  font-size: 10px;
}
img{
  width: 16%;
  height: 200px;
}
</style>
