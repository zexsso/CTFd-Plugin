<template>
	<div class="w-screen h-screen">
		<ctfChartVue />
		<ctfTableVue />
	</div>
	<ctfLastFlagger class="absolute right-0 bottom-0" />
	<ctfTop class="absolute left-0 bottom-0" />
	<ctfModalVue v-if="popupContent" :content="popupContent" />
	<ctfFailModal v-if="popupFail" :content="popupFail" />
</template>

<script setup>
	import ctfTableVue from "@/components/ctfTable.vue"
	import ctfChartVue from "@/components/ctfChart.vue"
	import ctfModalVue from "@/components/ctfModal.vue"
	import ctfFailModal from "./components/ctfFailModal.vue"
	import ctfLastFlagger from "@/components/ctfLast.vue"
	import ctfTop from "@/components/ctfTop.vue"
	import { ref } from "vue"
	import { useAppStore } from "@/stores/appStore"

	document.documentElement.classList.add("dark") // Enable dark mode for everyone

	const appStore = useAppStore()
	const popupContent = ref(false)
	const popupFail = ref(false)
	const popupDuration = 5000
	const popupInterval = 2000
	let popupQueueCount = 0
	let lasTriggerrTime = 0

	async function processQueue(type, data) {
		const nowTime = Date.now()
		const popupTime = popupInterval + popupDuration

		if (nowTime - lasTriggerrTime < popupTime) {
			++popupQueueCount
			const index = popupQueueCount
			const waitTime = (popupTime - (nowTime - lasTriggerrTime)) * popupQueueCount
			lasTriggerrTime = Date.now()
			console.log(index, " waiting", waitTime)
			await new Promise((r) => setTimeout(r, waitTime))
			console.log(index, " showing", waitTime)
		} else lasTriggerrTime = Date.now()

		if (type === "flag") {
			data["team_rank"] = getTeamRank(data)
			popupContent.value = data
		} else if (type === "fail") {
			popupFail.value = data
		}

		await new Promise((r) => setTimeout(r, popupDuration))

		if (type === "flag") popupContent.value = undefined
		else if (type === "fail") popupFail.value = undefined
		--popupQueueCount
	}

	appStore.socket.on("new-flag", (data) => {
		processQueue("flag", data)
	})

	appStore.socket.on("new-fail", (data) => {
		processQueue("fail", data)
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
