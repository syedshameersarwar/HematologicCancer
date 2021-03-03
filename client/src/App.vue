<template>
  <!-- <img id="ned" alt="Vue logo" src="./assets/logo.png" /> -->
  <!-- <HelloWorld msg="Early Screening and Detection of Hematologic Cancer using Complete Blood Count"/> -->
  <Main />
</template>

<script>
// import HelloWorld from "./components/Header/HelloWorld.vue";
import Main from "./components/Main.vue";

export default {
  name: "App",
  components: {
    // HelloWorld,
    Main
  },
  data: () => {
    return {};
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
  /* margin-top: 60px;
  font-size: 10px; */
}
/* img {
  width: 16%;
  height: 5%;
} */
</style>
