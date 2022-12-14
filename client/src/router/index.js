import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Главная',
      component: HomeView
    },
    {
      path: '/students',
      name: 'Факультеты',
      component: () => import('../views/FacultiesView.vue')
    },
    {
      path: '/students/:faculty_id',
      name: 'Группы',
      component: () => import('../views/FacultyView.vue'),
    },
    {
      path: '/students/:faculty_id/:group_id',
      name: 'Группа',
      component: () => import('../views/GroupView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'Страница не найдена',
      alias: '/404',
      component: () => import('../components/AppError.vue')
    },
  ]
});
router.beforeEach((to, from, next) => {
  document.title = to.name;
  window.scrollTo(0, 0)
  next();
});
export default router
