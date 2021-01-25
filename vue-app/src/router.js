import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/maze-js',
    name: 'Maze',
    component: () => import(/* webpackChunkName: "maze" */ '@/views/Maze.vue')
  },
  {
    path: '/maze-wasm',
    name: 'WasMaze',
    component: () => import(/* webpackChunkName: "maze" */ '@/views/Maze.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
