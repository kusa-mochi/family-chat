import Vue from "vue";
import Element from "element-ui";
import 'element-ui/lib/theme-chalk/index.css';
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.use(Element);
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: function (h) {
    return h(App);
  },
}).$mount("#app");
