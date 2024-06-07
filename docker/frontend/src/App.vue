<template>
	<div class="w-screen h-screen">
		<ctfChartVue />
		<ctfTableVue />
	</div>
	<ctfLastFlagger class="absolute right-0 bottom-0" />
	<ctfTop class="absolute left-0 bottom-0" />
	<ctfModalVue v-if="popupContent" :content="popupContent" />
</template>

<script setup>
	import ctfTableVue from "@/components/ctfTable.vue"
	import ctfChartVue from "@/components/ctfChart.vue"
	import ctfModalVue from "@/components/ctfModal.vue"
	import ctfLastFlagger from "@/components/ctfLast.vue"
	import ctfTop from "@/components/ctfTop.vue"
	import { ref } from "vue"
	import { useAppStore } from "@/stores/appStore"

	document.documentElement.classList.add("dark") // Enable dark mode for everyone

	const appStore = useAppStore()
	const popupContent = ref(false)
	let lastPopupTime
	const popupDuration = 5000
	const popupInterval = 2000

	appStore.socket.on("new-flag", async (data) => {
		console.log(data)
		const nowTime = Date.now()
		if (nowTime - lastPopupTime < popupInterval) {
			await new Promise((r) => setTimeout(r, popupInterval - (nowTime - lastPopupTime)))
		}
		data["team_rank"] = getTeamRank(data)
		popupContent.value = data
		await new Promise((r) => setTimeout(r, popupDuration))
		popupContent.value = undefined
		lastPopupTime = Date.now()
	})

	function getTeamRank(data) {
		const scoreboard = Object.keys(data.scoreboard).map((key) => ({
			...data.scoreboard[key],
			rank: parseInt(key),
		}))
		return scoreboard.findIndex((x) => x.name === data.team) + 1
	}
</script>

<style>
	html {
		scroll-behavior: smooth;
	}

	@font-face {
		font-family: "pcap_terminal";
		/* src: url("@/assets/fonts/pcap_terminal/PCap Terminal Condensed.otf"); */
		src: url("@/assets/fonts/hack/Hackout-Eaw5j.otf");
	}
	body {
		font-family: "pcap_terminal";
	}
</style>
