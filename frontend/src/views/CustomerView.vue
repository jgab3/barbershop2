<template>
  <div class="container">
    <h2>Customer Management</h2>

    <form @submit.prevent="submitForm">
      <input v-model="form.Firstname" placeholder="First Name" required />
      <input v-model="form.Lastname" placeholder="Last Name" required />
      <input v-model="form.Contact_Number" placeholder="Contact Number" required />
      <button type="submit">{{ editMode ? 'Update' : 'Add' }} Customer</button>
      <button type="button" v-if="editMode" @click="cancelEdit">Cancel</button>
    </form>

    <input v-model="search" placeholder="Search customers..." />

    <table>
      <thead>
        <tr>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Contact Number</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="customer in filteredCustomers" :key="customer.Customer_ID">
          <td>{{ customer.Firstname }}</td>
          <td>{{ customer.Lastname }}</td>
          <td>{{ customer.Contact_Number }}</td>
          <td>
            <button @click="editCustomer(customer)">Edit</button>
            <button @click="deleteCustomer(customer.Customer_ID)">Delete</button>
          </td>
        </tr>
        <tr v-if="filteredCustomers.length === 0">
          <td colspan="5" class="empty-state">No customers found.</td>
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
      customers: [],
      search: '',
      editMode: false,
      editId: null,
      form: { Firstname: '', Lastname: '', Contact_Number: '' }
    }
  },
  computed: {
    filteredCustomers() {
      return this.customers.filter(c =>
        c.Firstname.toLowerCase().includes(this.search.toLowerCase()) ||
        c.Lastname.toLowerCase().includes(this.search.toLowerCase())
      )
    }
  },
  mounted() { this.fetchCustomers() },
  methods: {
    async fetchCustomers() {
      const res = await axios.get(`${API}/customers`)
      this.customers = res.data
    },
    async submitForm() {
      if (this.editMode) {
        await axios.put(`${API}/customers/${this.editId}`, this.form)
      } else {
        await axios.post(`${API}/customers`, this.form)
      }
      this.fetchCustomers()
      this.resetForm()
    },
    editCustomer(customer) {
      this.editMode = true
      this.editId = customer.Customer_ID
      this.form.Firstname = customer.Firstname
      this.form.Lastname = customer.Lastname
      this.form.Contact_Number = customer.Contact_Number
    },
    async deleteCustomer(id) {
      if (confirm('Delete this customer?')) {
        await axios.delete(`${API}/customers/${id}`)
        this.fetchCustomers()
      }
    },
    cancelEdit() { this.resetForm() },
    resetForm() {
      this.editMode = false
      this.editId = null
      this.form = { Firstname: '', Lastname: '', Contact_Number: '' }
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