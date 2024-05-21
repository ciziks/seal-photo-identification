import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UploadSealView from '../views/UploadSealView.vue';
import DetectSealView from '../views/DetectSealView';
import ListSealsView from '../views/ListSealsView';
import AddSealView from '../views/AddSealView.vue';
import DeleteSealView from '../views/DeleteSealView.vue';
import AddSightingView from '../views/AddSightingView.vue';

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
    component: UploadSealView
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
  },
  {
    path: '/add-seal',
    name: 'add-seal',
    component: AddSealView
  },
  {
    path: '/delete-seal',
    name: 'delete-seal',
    component: DeleteSealView
  },
  {
    path: '/add-sighting',
    name: 'add-sighting',
    component: AddSightingView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
