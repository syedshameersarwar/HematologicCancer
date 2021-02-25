<template src="./Header.html"></template>
<script>
import testService from "../../services/test-service";

export default {
  name: "HelloWorld",
  props: {
    msg: String
  },
  data: () => {
    return {
      getRequest: "",
      apiResponse: "",
    };
  },
  methods: {
    async getMethod() {
      let response = await testService.testPythonApi();
      console.info(response);
      this.apiResponse = response.data;
    }, 
  }, 
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style src="./Header.css" scoped></style>
