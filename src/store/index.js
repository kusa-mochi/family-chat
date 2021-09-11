import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: "",
    userName: "",
    webSocketUrl:
      "wss://6o0lfe2404.execute-api.ap-northeast-1.amazonaws.com/production",
  },
  mutations: {
    setToken(state, token) {
      if (!token) return;
      state.token = token;
    },
    setUserName(state, userName) {
      if (!userName) return;
      state.userName = userName;
    },
  },
  actions: {
    setToken(context, token) {
      context.commit("setToken", token);
    },
    setUserName(context, userName) {
      context.commit("setUserName", userName);
    },
  },
  modules: {},
  plugins: [
    createPersistedState({
      key: "family-chat",
      storage: window.localStorage,
    }),
  ],
});
