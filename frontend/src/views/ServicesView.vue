<template>
  <div class="container">
    <h2>Service Management</h2>

    <form @submit.prevent="submitForm">
      <input v-model="form.Service_Name" placeholder="Service Name" required />
      <input v-model="form.Price" placeholder="Price" type="number" step="0.01" required />
      <button type="submit">{{ editMode ? 'Update' : 'Add' }} Service</button>
      <button type="button" v-if="editMode" @click="cancelEdit">Cancel</button>
    </form>

    <input v-model="search" placeholder="Search services..." />

    <table>
      <thead>
        <tr>
          <th>Service Name</th>
          <th>Price</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in filteredServices" :key="service.Services_Code">
          <td>{{ service.Service_Name }}</td>
          <td>₱{{ service.Price }}</td>
          <td>
            <button @click="editService(service)">Edit</button>
            <button @click="deleteService(service.Services_Code)">Delete</button>
          </td>
        </tr>
        <tr v-if="filteredServices.length === 0">
          <td colspan="4" class="empty-state">No services found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      services: [],
      search: '',
      editMode: false,
      editId: null,
      form: {
        Service_Name: '',
        Price: ''
      }
    }
  },
  computed: {
    filteredServices() {
      return this.services.filter(s =>
        s.Service_Name.toLowerCase().includes(this.search.toLowerCase())
      )
    }
  },
  mounted() {
    this.fetchServices()
  },
  methods: {
    async fetchServices() {
      const res = await axios.get(`${API}/services`)
      this.services = res.data
    },
    async submitForm() {
      if (this.editMode) {
        await axios.put(`${API}/services/${this.editId}`, this.form)
      } else {
        await axios.post(`${API}/services`, this.form)
      }
      this.fetchServices()
      this.resetForm()
    },
    editService(service) {
      this.editMode = true
      this.editId = service.Services_Code
      this.form.Service_Name = service.Service_Name
      this.form.Price = service.Price
    },
    async deleteService(id) {
      if (confirm('Delete this service?')) {
        await axios.delete(`${API}/services/${id}`)
        this.fetchServices()
      }
    },
    cancelEdit() {
      this.resetForm()
    },
    resetForm() {
      this.editMode = false
      this.editId = null
      this.form.Service_Name = ''
      this.form.Price = ''
    }
  }
}
</script>

<style scoped>
.container { padding: 20px; }
form { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
button { padding: 8px 16px; cursor: pointer; border-radius: 4px; border: none; background: #333; color: white; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
th { background: #333; color: white; }
</style>