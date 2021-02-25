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
      predictionResult: "",
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
      formData.append("file", this.file);
      let response = await testService.uploadCsv(formData);
      this.predictionResult = response.data;
      console.info(this.predictionResult);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style src="./Header.css" scoped></style>
