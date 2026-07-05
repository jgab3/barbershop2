<template>
  <div>
    <nav>
      <RouterLink to="/">Services</RouterLink>
      <RouterLink to="/barbers">Barbers</RouterLink>
      <RouterLink to="/customers">Customers</RouterLink>
      <RouterLink to="/reservations">Reservations</RouterLink>
    </nav>
    <RouterView />
  </div>
</template>

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
body {
  margin: 0;
  font-family: sans-serif;
}
</style>