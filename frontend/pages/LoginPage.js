export default {
  template: `
    <div>
        <h3>Login to QuizMaster</h3>
        <input placeholder="Email" v-model="email" />  
        <input placeholder="Password" type="password" v-model="password" />  
        <button class="btn btn-primary" @click="submitLogin">Login</button>
    </div>
  `,
  data() {
    return {
      email: null,
      password: null,
    };
  },
  methods: {
    async submitLogin() {
      const res = await fetch(location.origin + '/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: this.email, password: this.password })
      });

      if (res.ok) {
        const data = await res.json();
        console.log('✅ Logged in', data);

        // Store auth token & user info
        localStorage.setItem('token', data.token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('user_id', data.id);

        // Redirect to homepage or dashboard
        this.$router.push('/');
      } else {
        console.error('❌ Login failed');
        alert('Login failed. Please check your credentials.');
      }
    }
  }
}
