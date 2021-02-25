<template src="./Header.html"></template>
<script>
import testService from "../../services/test-service";
import VueCsvImport from "vue-csv-import";

export default {
  name: "HelloWorld",
  components: {
    VueCsvImport,
  },
  props: {
    msg: String,
  },
  data: () => {
    return {
      getRequest: "",
      apiResponse: "",
      csv: null,
      file: "",
    };
  },
  methods: {
    async getMethod() {
      let response = await testService.testPythonApi();
      console.info(response);
      this.apiResponse = response.data;
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
    async submitFile() {
      let formData = new FormData();
      console.info(this.file);
      formData.append("file", this.file);
      console.info(formData);
      // let body = "hello gutentag";
      let response = testService.uploadCsv(formData);
      console.info(response);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style src="./Header.css" scoped></style>
