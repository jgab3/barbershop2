<template>
  <div class="container">
    <h2>Reservation Management</h2>

    <form @submit.prevent="submitForm">
      <select v-model="form.Customer_ID" required>
        <option value="" disabled>Select Customer</option>
        <option v-for="c in customers" :key="c.Customer_ID" :value="c.Customer_ID">
          {{ c.Firstname }} {{ c.Lastname }}
        </option>
      </select>
      <select v-model="form.Barber_ID" required>
        <option value="" disabled>Select Barber</option>
        <option v-for="b in barbers" :key="b.Barber_ID" :value="b.Barber_ID">
          {{ b.Barber_Name }}
        </option>
      </select>
      <input v-model="form.Date" type="date" required />
      <input v-model="form.Time" type="time" required />
      <input v-model="form.DP_Amount" type="number" step="0.01" placeholder="DP Amount" required />
      <select v-model="form.Status">
        <option>Pending</option>
        <option>Confirmed</option>
        <option>Cancelled</option>
        <option>Completed</option>
        <option>No-show</option>
      </select>
      <button type="submit">{{ editMode ? 'Update' : 'Add' }} Reservation</button>
      <button type="button" v-if="editMode" @click="cancelEdit">Cancel</button>
    </form>

    <input v-model="search" placeholder="Search reservations..." />

    <table>
      <thead>
        <tr>
          <th>Customer</th>
          <th>Barber</th>
          <th>Date</th>
          <th>Time</th>
          <th>Status</th>
          <th>DP Amount</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in filteredReservations" :key="r.Reservation_ID">
          <td>{{ r.Customer_Name }}</td>
          <td>{{ r.Barber_Name }}</td>
          <td>{{ r.Date }}</td>
          <td>{{ formatTime(r.Time) }}</td>
          <td>
              <span :class="'badge badge-' + r.Status.toLowerCase().replace('-', '')">
                 {{ r.Status }}
              </span>
          </td>
          <td>₱{{ r.DP_Amount }}</td>
          <td>
            <button @click="editReservation(r)">Edit</button>
            <button @click="deleteReservation(r.Reservation_ID)">Delete</button>
          </td>
        </tr>
            <tr v-if="filteredReservations.length === 0">
              <td colspan="8" class="empty-state">No reservations found.</td>
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
      reservations: [],
      customers: [],
      barbers: [],
      search: '',
      editMode: false,
      editId: null,
      form: {
        Customer_ID: '',
        Barber_ID: '',
        Date: '',
        Time: '',
        DP_Amount: '',
        Status: 'Pending'
      }
    }
  },
  computed: {
    filteredReservations() {
      return this.reservations.filter(r =>
        r.Customer_Name.toLowerCase().includes(this.search.toLowerCase()) ||
        r.Barber_Name.toLowerCase().includes(this.search.toLowerCase()) ||
        r.Status.toLowerCase().includes(this.search.toLowerCase())
      )
    }
  },
  mounted() {
    this.fetchReservations()
    this.fetchCustomers()
    this.fetchBarbers()
  },
  methods: {
    async fetchReservations() {
      const res = await axios.get(`${API}/reservations`)
      this.reservations = res.data
    },
    async fetchCustomers() {
      const res = await axios.get(`${API}/customers`)
      this.customers = res.data
    },
    async fetchBarbers() {
      const res = await axios.get(`${API}/barbers`)
      this.barbers = res.data
    },
    formatTime(time) {
        if (!time) return ''
        const [hours, minutes] = time.split(':')
        const h = parseInt(hours)
        const ampm = h >= 12 ? 'PM' : 'AM'
        const hour12 = h % 12 || 12
      return `${hour12}:${minutes} ${ampm}`
    },
    async submitForm() {
        try {
          if (this.editMode) {
             await axios.put(`${API}/reservations/${this.editId}`, this.form)
          } else {
           await axios.post(`${API}/reservations`, this.form)
      }
        this.fetchReservations()
        this.resetForm()
      } catch (error) {
        alert(error.response.data.message)
      }
    },
    editReservation(r) {
      this.editMode = true
      this.editId = r.Reservation_ID
      this.form.Customer_ID = r.Customer_ID
      this.form.Barber_ID = r.Barber_ID
      this.form.Date = r.Date
      this.form.Time = r.Time
      this.form.DP_Amount = r.DP_Amount
      this.form.Status = r.Status
    },
    async deleteReservation(id) {
      if (confirm('Delete this reservation?')) {
        await axios.delete(`${API}/reservations/${id}`)
        this.fetchReservations()
      }
    },
    cancelEdit() { this.resetForm() },
    resetForm() {
      this.editMode = false
      this.editId = null
      this.form = {
        Customer_ID: '',
        Barber_ID: '',
        Date: '',
        Time: '',
        DP_Amount: '',
        Status: 'Pending'
      }
    }
  }
}
</script>

<style scoped>
.container { padding: 20px; }
form { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
input, select { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
button { padding: 8px 16px; cursor: pointer; border-radius: 4px; border: none; background: #333; color: white; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
th { background: #333; color: white; }
</style>