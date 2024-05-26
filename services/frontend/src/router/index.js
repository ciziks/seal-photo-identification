import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ListSealsView from '../views/ListSealsView';
import AddSealView from '../views/AddSealView.vue';
import DeleteSealView from '../views/DeleteSealView.vue';
import AddSightingView from '../views/AddSightingView.vue';
import DeleteSightingView from '../views/DeleteSightingView.vue';
import ListSightingView from '../views/ListSightingView.vue';
import SealDetailsView from '../views/SealDetailsView.vue';
import FindSealView from '../views/FindSealView.vue';
import UserGuideView from '../views/UserGuideView.vue';

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
  },
  {
    path: '/delete-sighting',
    name: 'delete-sighting',
    component: DeleteSightingView
  },
  {
    path: '/list-sighting',
    name: 'list-sighting',
    component: ListSightingView
  },
  {
    path: '/seal/:sealId',
    name: 'SealDetails',
    component: SealDetailsView,
    props: true,
  },
  {
    path: '/find-seal',
    name: 'FindSeal',
    component: FindSealView,
  },
  {
    path: '/user-guide',
    name: 'userGuide',
    component: UserGuideView,
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
