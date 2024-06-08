<template>
	<div class="w-screen h-screen">
		<ctfChartVue />
		<ctfTableVue />
	</div>
	<ctfLastFlagger class="absolute right-0 bottom-0" />
	<ctfTop class="absolute left-0 bottom-0" />
	<ctfModalVue v-if="popupContent" :content="popupContent" />
	<ctfFailModal v-if="popupFail" :content="popupFail" />
	<img src="@/assets/images/ctflogo.png" alt="ctflogo" class="absolute left-0 top-0 m-4 w-44" />
	<audio ref="audio" muted></audio>
	<button v-if="isMuted" @click="unmuteAudio" class="absolute bottom-10 left-10 p-2 bg-gray-700 text-white rounded">
		Unmute
	</button>
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

	import categoryCompleteAudio from "@/assets/audio/category_complete.mp3"
	import defuseBombAudio from "@/assets/audio/defuse_bomb.mp3"
	import firstBloodAudio from "@/assets/audio/first_blood.mp3"
	import solvedAudio from "@/assets/audio/solved.mp3"
	import failAudio from "@/assets/audio/fail.mp3"

	document.documentElement.classList.add("dark") // Enable dark mode for everyone

	const appStore = useAppStore()
	const popupContent = ref(false)
	const popupFail = ref(false)
	const popupDuration = 5000
	const popupInterval = 2000
	let popupQueueCount = 0
	let lasTriggerrTime = 0
	const audio = ref(null)
	const isMuted = ref(true)

	function playAudio(src) {
		if (audio.value) {
			audio.value.src = src
			audio.value.play().catch((error) => {
				console.error("Failed to play audio:", error)
			})
		}
	}

	function unmuteAudio() {
		if (audio.value) {
			audio.value.muted = false
			console.log("Audio unmuted")
			isMuted.value = false
		}
	}

	async function showModal(type, data) {
		const nowTime = Date.now()
		const popupTime = popupInterval + popupDuration

		if (nowTime - lasTriggerrTime < popupTime) {
			const waitTime = popupTime - (nowTime - lasTriggerrTime)
			lasTriggerrTime = Date.now()
			await new Promise((r) => setTimeout(r, waitTime))
		} else lasTriggerrTime = Date.now()
		

		if (type === "flag") {
			data["team_rank"] = getTeamRank(data)
			popupContent.value = data

			if (data.is_category_complete) playAudio(categoryCompleteAudio)
			else if (data.challenge === "") playAudio(defuseBombAudio)
			else if (data.solve_id === 0) playAudio(firstBloodAudio)
			else if (data.solve_id > 0) playAudio(solvedAudio)
		} else if (type === "fail") {
			popupFail.value = data
			if (Math.random() < 0.25) {
				playAudio(failAudio)
			}
		}

		await new Promise((r) => setTimeout(r, popupDuration))

		if (type === "flag") popupContent.value = undefined
		else if (type === "fail") popupFail.value = undefined
	}

	appStore.socket.on("new-flag", (data) => {
		showModal("flag", data)
	})

	appStore.socket.on("new-fail", (data) => {
		showModal("fail", data)
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
		font-family: "hackout";
		src: url("@/assets/fonts/hackout/hackout.otf");
	}
	body {
		font-family: "hackout";
	}
</style>
