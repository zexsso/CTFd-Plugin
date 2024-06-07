<template>
	<div>
		<h1 class="text-center font-bold text-xl">Last Solve</h1>
		<div class="rounded-xl border m-4 p-5" v-if="lastFlagger">
			<div class="flex justify-between space-x-4">
				<div class="flex space-x-2">
					<p class="font-bold">Category:</p>
					<p class="text-[#20C20E]">{{ lastFlagger.category }}</p>
				</div>
				<div class="flex space-x-2">
					<p class="font-bold">Challenge:</p>
					<p class="text-[#20C20E]">{{ lastFlagger.challenge }}</p>
				</div>
			</div>
			<div class="flex justify-between space-x-4">
				<div class="flex space-x-2">
					<p class="font-bold">Team:</p>
					<p class="text-[#20C20E]">{{ lastFlagger.team }}</p>
				</div>
				<div class="flex space-x-2">
					<p class="font-bold">User:</p>
					<p class="text-[#20C20E]">{{ lastFlagger.user }}</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref } from "vue"
	import { useAppStore } from "@/stores/appStore"

	const appStore = useAppStore()
	const lastFlagger = ref()
	appStore.socket.on("new-flag", async (data) => {
		lastFlagger.value = data
	})
</script>
