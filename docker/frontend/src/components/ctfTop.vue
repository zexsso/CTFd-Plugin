<template>
	<div>
		<div class="rounded-xl border m-4 p-5" v-if="topFlagger">
			<h1 class="text-center font-bold text-xl">Most Solves</h1>
			<div class="flex space-x-2 mt-4 items-center">
				<p class="text-[#20C20E]">{{ topFlagger.user_name }}</p>
				<p class="text-[#20C20E]">{{ topFlagger.user_team }}</p>
				<p>{{ topFlagger.correct_count }}</p>
                <p>👑</p>
			</div>
		</div>
		<div class="rounded-xl border m-4 p-5" v-if="topFailer">
			<h1 class="text-center font-bold text-xl">Most Fails</h1>
			<div class="flex space-x-2 mt-4 items-center">
				<p class="text-[#20C20E]">{{ topFailer.user_name }}</p>
				<p class="text-[#20C20E]">{{ topFailer.user_team }}</p>
				<p>{{ topFailer.incorrect_count }}</p>
                <p>💩</p>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref } from "vue"
	import { useAppStore } from "@/stores/appStore"

	const appStore = useAppStore()
	const topFlagger = ref()
	const topFailer = ref()
	appStore.socket.on("new-flag", async (data) => {
		topFlagger.value = data.top_flagger
		topFailer.value = data.top_failer
	})

	appStore.socket.on("new-fail", async (data) => {
		topFailer.value = data.top_failer
	})
</script>
