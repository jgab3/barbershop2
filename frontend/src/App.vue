<template>
  <div>
    <nav v-if="$route.name !== 'login'">
      <RouterLink to="/">Services</RouterLink>
      <RouterLink to="/barbers">Barbers</RouterLink>
      <RouterLink to="/customers">Customers</RouterLink>
      <RouterLink to="/reservations">Reservations</RouterLink>
      <button class="logout-btn" @click="logout">Logout</button>
    </nav>
    <RouterView />
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    logout() {
      localStorage.removeItem('barberease_user')
      this.$router.push('/login')
    }
  }
}
</script>

<style>
nav {
  display: flex;
  gap: 16px;
  padding: 14px 20px;
  background: #1a1a1a;
}
nav a {
  color: white;
  text-decoration: none;
  font-size: 15px;
  padding: 6px 14px;
  border-radius: 4px;
}
nav a:hover, nav a.router-link-active {
  background: #444;
}
.logout-btn {
  margin-left: auto;
  background: transparent;
  border: 1px solid #555;
  color: #ccc;
}
.logout-btn:hover {
  background: #444;
  color: white;
}
body {
  margin: 0;
  font-family: sans-serif;
}
</style>