import { createRouter, createWebHistory } from 'vue-router'
import ServicesView from '../views/ServicesView.vue'
import BarberView from '../views/BarberView.vue'
import CustomerView from '../views/CustomerView.vue'
import ReservationView from '../views/ReservationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'services', component: ServicesView },
    { path: '/barbers', name: 'barbers', component: BarberView },
    { path: '/customers', name: 'customers', component: CustomerView },
    { path: '/reservations', name: 'reservations', component: ReservationView }
  ]
})

export default router