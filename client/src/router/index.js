import Vue from 'vue';
import Router from 'vue-router';
import System from '../views/System';
import Different from '../views/Different';
import Compare from '../views/Compare';
import Multilayer from '../views/Multilayer';
import Accompany from '../views/Accompany';
import NetworkAnalysis from '../views/NetworkAnalysis';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'System',
      component: System
    },
    {
      path: '/networkAnalysis',
      name: 'NetworkAnalysis',
      component: NetworkAnalysis
    },
    {
      path: '/different',
      name: 'different',
      component: Different
    },
    {
      path: '/compare',
      name: 'compare',
      component: Compare
    },
    {
      path: '/accompany',
      name: 'accompany',
      component: Accompany
    },
    {
      path: '/multilayer',
      name: 'multilayer',
      component: Multilayer
    }
  ]
});
