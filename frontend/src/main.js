import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";

//PrimeVue
import PrimeVue from "primevue/config";
import "primevue/resources/themes/aura-dark-noir/theme.css"
import setupPrimeVue from "./primeVueSetup"

// Tailwind setup + custom preflight
import "./assets/styles/base.css"

// Material Icons
import "material-icons/iconfont/material-icons.css";

import ToastService from 'primevue/toastservice';

const app = createApp(App);

app.use(createPinia());
app.use(ToastService);
app.use(PrimeVue);
setupPrimeVue(app);

app.mount("#app");