import Vue from "vue";
import App from "./App.vue";
import Quasar from 'quasar';
import QFile from 'quasar';

Vue.config.productionTip = false;

new Vue({
  render: h => h(App)
}).$mount("#app");

Vue.use(Quasar, {
  components: {
    QFile
  }
});
