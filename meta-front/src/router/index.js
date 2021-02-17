import Vue from "vue";
import VueRouter from "vue-router";
import ProfileList from "../views/ProfileList.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "profile-list",
    component: ProfileList
  },
  {
    path: "/profile/:id",
    name: "profile-show",
    component: () => import("../views/ProfileShow.vue"),
    props: true
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

export default router;
