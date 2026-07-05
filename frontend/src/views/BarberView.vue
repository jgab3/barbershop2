<template>
  <div class="container">
    <h2>Barber Management</h2>

    <form @submit.prevent="submitForm">
      <input v-model="form.Barber_Name" placeholder="Barber Name" required />
      <input v-model="form.Contact_Number" placeholder="Contact Number" required />
      <button type="submit">{{ editMode ? 'Update' : 'Add' }} Barber</button>
      <button type="button" v-if="editMode" @click="cancelEdit">Cancel</button>
    </form>

    <input v-model="search" placeholder="Search barbers..." />

    <table>
      <thead>
        <tr>
          <th>Barber Name</th>
          <th>Contact Number</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="barber in filteredBarbers" :key="barber.Barber_ID">
          <td>{{ barber.Barber_Name }}</td>
          <td>{{ barber.Contact_Number }}</td>
          <td>
            <button @click="editBarber(barber)">Edit</button>
            <button @click="deleteBarber(barber.Barber_ID)">Delete</button>
            <button @click="viewSchedule(barber)">Schedule</button>
          </td>
        </tr>
        <tr v-if="filteredBarbers.length === 0">
            <td colspan="4" class="empty-state">No barbers found.</td>
        </tr>
      </tbody>
    </table>

    <div v-if="selectedBarber" class="schedule-section">
      <h3>Schedule for {{ selectedBarber.Barber_Name }}</h3>

      <form @submit.prevent="submitSchedule">
        <select v-model="scheduleForm.Day" required>
          <option value="" disabled>Select Day</option>
          <option>Monday</option>
          <option>Tuesday</option>
          <option>Wednesday</option>
          <option>Thursday</option>
          <option>Friday</option>
          <option>Saturday</option>
          <option>Sunday</option>
        </select>
        <input v-model="scheduleForm.Start_Time" type="time" required />
        <input v-model="scheduleForm.End_Time" type="time" required />
        <button type="submit">{{ scheduleEditMode ? 'Update' : 'Add' }} Schedule</button>
        <button type="button" v-if="scheduleEditMode" @click="cancelScheduleEdit">Cancel</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>Day</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in schedules" :key="s.Schedule_ID">
            <td>{{ s.Day }}</td>
            <td>{{ formatTime(s.Start_Time) }}</td>
            <td>{{ formatTime(s.End_Time) }}</td>
            <td>
              <button @click="editSchedule(s)">Edit</button>
              <button @click="deleteSchedule(s.Schedule_ID)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      barbers: [],
      search: '',
      editMode: false,
      editId: null,
      form: { Barber_Name: '', Contact_Number: '' },
      selectedBarber: null,
      schedules: [],
      scheduleEditMode: false,
      scheduleEditId: null,
      scheduleForm: { Day: '', Start_Time: '', End_Time: '' }
    }
  },
  computed: {
    filteredBarbers() {
      return this.barbers.filter(b =>
        b.Barber_Name.toLowerCase().includes(this.search.toLowerCase())
      )
    }
  },
  mounted() { this.fetchBarbers() },
  methods: {
    async fetchBarbers() {
      const res = await axios.get(`${API}/barbers`)
      this.barbers = res.data
    },
    async submitForm() {
      if (this.editMode) {
        await axios.put(`${API}/barbers/${this.editId}`, this.form)
      } else {
        await axios.post(`${API}/barbers`, this.form)
      }
      this.fetchBarbers()
      this.resetForm()
    },
    editBarber(barber) {
      this.editMode = true
      this.editId = barber.Barber_ID
      this.form.Barber_Name = barber.Barber_Name
      this.form.Contact_Number = barber.Contact_Number
    },
    async deleteBarber(id) {
      if (confirm('Delete this barber?')) {
       try {
      await axios.delete(`${API}/barbers/${id}`)
      this.fetchBarbers()
           if (this.selectedBarber && this.selectedBarber.Barber_ID === id) {
        this.selectedBarber = null
        this.schedules = []
        }
      } catch (error) {
         alert(error.response.data.message)
        }
      }
    },
      
    cancelEdit() { this.resetForm() },
    resetForm() {
      this.editMode = false
      this.editId = null
      this.form = { Barber_Name: '', Contact_Number: '' }
    },
    async viewSchedule(barber) {
      this.selectedBarber = barber
      const res = await axios.get(`${API}/barbers/${barber.Barber_ID}/schedules`)
      this.schedules = res.data
    },
    async submitSchedule() {
      if (this.scheduleEditMode) {
        await axios.put(`${API}/schedules/${this.scheduleEditId}`, this.scheduleForm)
      } else {
        await axios.post(`${API}/barbers/${this.selectedBarber.Barber_ID}/schedules`, this.scheduleForm)
      }
      this.viewSchedule(this.selectedBarber)
      this.resetScheduleForm()
    },
    editSchedule(s) {
      this.scheduleEditMode = true
      this.scheduleEditId = s.Schedule_ID
      this.scheduleForm.Day = s.Day
      this.scheduleForm.Start_Time = s.Start_Time
      this.scheduleForm.End_Time = s.End_Time
    },
    async deleteSchedule(id) {
      if (confirm('Delete this schedule?')) {
        await axios.delete(`${API}/schedules/${id}`)
        this.viewSchedule(this.selectedBarber)
      }
    },
    cancelScheduleEdit() { this.resetScheduleForm() },
    resetScheduleForm() {
      this.scheduleEditMode = false
      this.scheduleEditId = null
      this.scheduleForm = { Day: '', Start_Time: '', End_Time: '' }
    },

    formatTime(time) {
        if (!time) return ''
         const [hours, minutes] = time.split(':')
        const h = parseInt(hours)
        const ampm = h >= 12 ? 'PM' : 'AM'
        const hour12 = h % 12 || 12
        return `${hour12}:${minutes} ${ampm}`
    }
  }
}
</script>

<style scoped>
.container { padding: 20px; }
form { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
input, select { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
button { padding: 8px 16px; cursor: pointer; border-radius: 4px; border: none; background: #333; color: white; }
table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
th { background: #333; color: white; }
.schedule-section { margin-top: 30px; border-top: 2px solid #333; padding-top: 20px; }
.schedule-section h3 { margin-bottom: 16px; }
</style>