<template>
	<div class="w-screen h-screen">
		<ctfChartVue />
		<ctfTableVue />
	</div>
</template>

<script setup>
	import ctfTableVue from "@/components/ctfTable.vue"
	import ctfChartVue from "@/components/ctfChart.vue"
	import ctfModalVue from "@/components/ctfModal.vue"
	import { onMounted, onUnmounted } from "vue"
	import { useToast } from "primevue/usetoast"
	import { useAppStore } from "./stores/appStore"

	document.documentElement.classList.add("dark") // Enable dark mode for everyone

	const appStore = useAppStore()
	// appStore.toast = useToast()

	onMounted(() => {
    appStore.connectSocket()
  })

  onUnmounted(() => {
    appStore.socket.disconnect()
  })
</script>
