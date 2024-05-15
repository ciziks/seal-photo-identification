import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AddSealView from '../views/UploadSealView.vue';
import DetectSealView from '../views/DetectSealView';
import ListSealsView from '../views/ListSealsView';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/upload-seal',
    name: 'upload-seal',
    component: AddSealView
  },
  {
    path: '/detect-seal',
    name: 'detect-seal',
    component: DetectSealView
  },
  {
    path: '/list-seals',
    name: 'list-seals',
    component: ListSealsView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
