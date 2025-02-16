import { createApp } from 'vue'
import App from './App.vue'


// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { createRouter, createWebHashHistory } from 'vue-router'
import CardStatsContainer from './components/CardStatsContainer'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/home', component: CardStatsContainer },
        { path: '/', redirect: '/home' }
    ]
})

createApp(App).use(router).mount('#app')
