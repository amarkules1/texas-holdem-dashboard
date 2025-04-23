import { createApp } from 'vue'
import App from './App.vue'


// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import "bootstrap"
import { createRouter, createWebHashHistory } from 'vue-router'
import CardStatsContainer from './components/CardStatsContainer'
import ResourcesComponent from './components/ResourcesComponent.vue'
import HandComparison from './components/HandComparison.vue'
import PlayerStats from './components/PlayerStats.vue'
import OutsTracker from './components/OutsTracker.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/home', component: CardStatsContainer },
        { path: '/resources', component: ResourcesComponent },
        { path: '/hand-comparison', component: HandComparison},
        { path: '/player-stats', component: PlayerStats},
        { path: '/outs-tracker', component: OutsTracker},
        { path: '/', redirect: '/home' }
    ]
})

createApp(App).use(router).mount('#app')
