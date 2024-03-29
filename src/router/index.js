import Vue from "vue";
import VueRouter from "vue-router";
import Login from "@/views/Login.vue";
import Chat from "@/views/Chat.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  {
    path: "/chat",
    name: "Chat",
    component: Chat,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
