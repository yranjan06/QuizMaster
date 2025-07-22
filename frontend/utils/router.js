const Home = {
  template: `<h1>Welcome to QuizMaster</h1>`
}

import LoginPage from "../pages/LoginPage.js";
import RegisterPage from "../pages/RegisterPage.js";

// All routes used in QuizMaster App
const routes = [
  { path: '/', component: Home },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
]

// Router instance setup
const router = new VueRouter({
  routes
})

export default router;
