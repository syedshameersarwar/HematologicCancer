import Vue from "vue";
import App from "./App.vue";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import VueApexCharts from "vue-apexcharts";

Vue.use(VueApexCharts);
Vue.component("apexchart", VueApexCharts);

Vue.use(Antd);

Vue.config.productionTip = false;

new Vue({
  render: h => h(App)
}).$mount("#app");
