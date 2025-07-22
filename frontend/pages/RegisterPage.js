export default {
  template: `
    <div>
        <h3>Register for QuizMaster</h3>
        <input placeholder="Email" v-model="email" />
        <input placeholder="Password" type="password" v-model="password" />
        <input placeholder="Role (user or admin)" v-model="role" />
        <button class="btn btn-primary" @click="submitRegister">Register</button>
    </div>
  `,
  data() {
    return {
      email: null,
      password: null,
      role: 'user',  // default to user
    };
  },
  methods: {
    async submitRegister() {
      const res = await fetch(location.origin + '/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: this.email,
          password: this.password,
          role: this.role
        })
      });

      if (res.ok) {
        const data = await res.json();
        console.log('✅ Registered', data);
        alert('Registration successful');
        this.$router.push('/login');
      } else {
        const err = await res.json();
        console.error('❌ Registration failed', err);
        alert(err.message || 'Registration failed');
      }
    }
  }
}
