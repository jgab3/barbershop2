<template>
  <div class="auth-page">
    <div class="auth-panel">
      <div class="brand">
        <div class="brand-icon">✂</div>
        <h1>BarberEase</h1>
        <p>Your time. Your style. Our priority.</p>
      </div>
    </div>

    <div class="auth-form-wrap">
      <div class="tabs">
        <button
          type="button"
          :class="{ active: mode === 'login' }"
          @click="switchMode('login')"
        >Login</button>
        <button
          type="button"
          :class="{ active: mode === 'register' }"
          @click="switchMode('register')"
        >Register</button>
      </div>

      <h2 class="title">{{ mode === 'login' ? 'Welcome back!' : 'Create your account' }}</h2>
      <p class="subtitle">
        {{ mode === 'login' ? 'Login to continue to your account.' : 'Register to start booking appointments.' }}
      </p>

      <div v-if="feedback.text" :class="['feedback', feedback.type]">
        {{ feedback.text }}
      </div>

      <form @submit.prevent="mode === 'login' ? handleLogin() : handleRegister()" novalidate>
        <template v-if="mode === 'register'">
          <label>First Name</label>
          <input v-model.trim="form.Firstname" type="text" placeholder="Enter your first name" />
          <span class="field-error" v-if="errors.Firstname">{{ errors.Firstname }}</span>

          <label>Last Name</label>
          <input v-model.trim="form.Lastname" type="text" placeholder="Enter your last name" />
          <span class="field-error" v-if="errors.Lastname">{{ errors.Lastname }}</span>
        </template>

        <label>Email Address</label>
        <input v-model.trim="form.Email" type="email" placeholder="Enter your email" />
        <span class="field-error" v-if="errors.Email">{{ errors.Email }}</span>

        <label>Password</label>
        <input v-model="form.Password" type="password" placeholder="Enter your password" />
        <span class="field-error" v-if="errors.Password">{{ errors.Password }}</span>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Please wait...' : (mode === 'login' ? 'Login' : 'Register') }}
        </button>
      </form>

      <p class="switch-line">
        <template v-if="mode === 'login'">
          Don't have an account?
          <a href="#" @click.prevent="switchMode('register')">Register</a>
        </template>
        <template v-else>
          Already have an account?
          <a href="#" @click.prevent="switchMode('login')">Login</a>
        </template>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const API = 'http://127.0.0.1:5000'

export default {
  name: 'LoginView',
  data() {
    return {
      mode: 'login',
      loading: false,
      feedback: { text: '', type: '' },
      form: {
        Firstname: '',
        Lastname: '',
        Email: '',
        Password: ''
      },
      errors: {}
    }
  },
  methods: {
    switchMode(mode) {
      this.mode = mode
      this.errors = {}
      this.feedback = { text: '', type: '' }
    },
    validate() {
      const errors = {}

      if (this.mode === 'register') {
        if (!this.form.Firstname) errors.Firstname = 'First name is required.'
        if (!this.form.Lastname) errors.Lastname = 'Last name is required.'
      }

      if (!this.form.Email) {
        errors.Email = 'Email is required.'
      } else if (!/^\S+@\S+\.\S+$/.test(this.form.Email)) {
        errors.Email = 'Enter a valid email address.'
      }

      if (!this.form.Password) {
        errors.Password = 'Password is required.'
      } else if (this.mode === 'register' && this.form.Password.length < 6) {
        errors.Password = 'Password must be at least 6 characters.'
      }

      this.errors = errors
      return Object.keys(errors).length === 0
    },
    async handleLogin() {
      this.feedback = { text: '', type: '' }
      if (!this.validate()) return

      this.loading = true
      try {
        const res = await axios.post(`${API}/api/login`, {
          Email: this.form.Email,
          Password: this.form.Password
        })
        localStorage.setItem('barberease_user', JSON.stringify(res.data.user))
        this.feedback = { text: res.data.message, type: 'success' }
        this.$router.push('/')
      } catch (err) {
        this.feedback = {
          text: err.response?.data?.message || 'Invalid login. Please try again.',
          type: 'error'
        }
      } finally {
        this.loading = false
      }
    },
    async handleRegister() {
      this.feedback = { text: '', type: '' }
      if (!this.validate()) return

      this.loading = true
      try {
        const res = await axios.post(`${API}/api/register`, this.form)
        this.feedback = { text: res.data.message, type: 'success' }
        this.mode = 'login'
        this.form.Password = ''
      } catch (err) {
        this.feedback = {
          text: err.response?.data?.message || 'Registration failed. Please try again.',
          type: 'error'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  min-height: 100vh;
}

.auth-panel {
  flex: 1;
  background: linear-gradient(160deg, #1a1a2e, #16213e);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.brand {
  text-align: center;
  padding: 40px;
}

.brand-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.brand h1 {
  font-size: 36px;
  margin-bottom: 8px;
}

.brand p {
  color: #cfd2e0;
  font-size: 15px;
}

.auth-form-wrap {
  flex: 1;
  max-width: 480px;
  margin: auto;
  padding: 40px;
}

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 1px solid #eee;
}

.tabs button {
  background: none;
  border: none;
  padding: 10px 4px;
  margin-right: 24px;
  font-size: 15px;
  font-weight: 600;
  color: #999;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tabs button.active {
  color: #1a1a1a;
  border-bottom-color: #1a1a2e;
}

.title {
  font-size: 22px;
  margin-bottom: 4px;
  border: none;
  padding: 0;
}

.subtitle {
  color: #777;
  font-size: 14px;
  margin-bottom: 20px;
}

.feedback {
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 14px;
  margin-bottom: 16px;
}

.feedback.success {
  background: #d1fae5;
  color: #065f46;
}

.feedback.error {
  background: #fee2e2;
  color: #991b1b;
}

form {
  display: block;
  background: none;
  box-shadow: none;
  padding: 0;
  margin-bottom: 0;
}

label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 6px;
  margin-top: 14px;
  color: #333;
}

form input {
  width: 100%;
}

.field-error {
  display: block;
  color: #c53030;
  font-size: 12px;
  margin-top: 4px;
}

.submit-btn {
  width: 100%;
  margin-top: 24px;
  padding: 12px;
  font-size: 15px;
  background: #1a1a2e;
}

.submit-btn:hover {
  background: #16213e;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.switch-line {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #777;
}

.switch-line a {
  color: #1a1a2e;
  font-weight: 600;
  text-decoration: none;
}

@media (max-width: 800px) {
  .auth-page {
    flex-direction: column;
  }
  .auth-panel {
    padding: 30px 0;
  }
}
</style>
