import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import ServicesView from '../views/ServicesView.vue'
import BarberView from '../views/BarberView.vue'
import CustomerView from '../views/CustomerView.vue'
import ReservationView from '../views/ReservationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'login', component: LoginView, meta: { public: true } },
    { path: '/', name: 'services', component: ServicesView },
    { path: '/barbers', name: 'barbers', component: BarberView },
    { path: '/customers', name: 'customers', component: CustomerView },
    { path: '/reservations', name: 'reservations', component: ReservationView }
  ]
})

router.beforeEach((to) => {
  const isLoggedIn = !!localStorage.getItem('barberease_user')
  if (!to.meta.public && !isLoggedIn) {
    return { name: 'login' }
  }
  if (to.name === 'login' && isLoggedIn) {
    return { name: 'services' }
  }
  return true
})

export default router