import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';
import Profile from '../views/Profile.vue';
import Settings from '../views/Settings.vue';
import Auth from '../views/Auth.vue';
import Register from "../views/Register.vue";
import Login from "../views/Login.vue";

const routes = [
  { path: '/', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/settings', component: Settings, meta: { requiresAuth: true } },
  { path: '/auth', component: Auth },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Глобальный guard для проверки токена
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  if (to.meta.requiresAuth && !token) {
    next('/auth');
  } else {
    next();
  }
});

export default router;
