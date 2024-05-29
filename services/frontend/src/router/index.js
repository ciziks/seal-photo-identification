import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ListSealsView from '../views/ListSealsView';
import NewSealView from '../views/NewSealView.vue';
import DeleteSealView from '../views/DeleteSealView.vue';
import NewSightingView from '../views/NewSightingView.vue';
import DeleteSightingView from '../views/DeleteSightingView.vue';
import FindSightingView from '../views/FindSightingView.vue';
import SealDetailsView from '../views/SealDetailsView.vue';
import FindSealView from '../views/FindSealView.vue';
import UserGuideView from '../views/UserGuideView.vue';
import ExportView from '../views/ExportView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/list-seals',
    name: 'list-seals',
    component: ListSealsView
  },
  {
    path: '/new-seal',
    name: 'new-seal',
    component: NewSealView
  },
  {
    path: '/delete-seal',
    name: 'delete-seal',
    component: DeleteSealView
  },
  {
    path: '/new-sighting',
    name: 'new-sighting',
    component: NewSightingView
  },
  {
    path: '/delete-sighting',
    name: 'delete-sighting',
    component: DeleteSightingView
  },
  {
    path: '/find-sighting',
    name: 'find-sighting',
    component: FindSightingView
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
  },
  {
    path: '/export',
    name: 'export',
    component: ExportView,
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
