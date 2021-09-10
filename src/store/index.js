import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: "",
    webSocketUrl:
      "wss://6o0lfe2404.execute-api.ap-northeast-1.amazonaws.com/production",
  },
  mutations: {},
  actions: {},
  modules: {},
});
