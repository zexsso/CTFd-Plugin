<template>
	<div class="flex justify-center h-[60vh] mx-auto">
		<div ref="tableContainer" class="overflow-auto h-full no-scrollbar">
			<table class="table-auto w-full">
				<thead class="sticky top-0 bg-[#2a2a2a] text-[#FF005C]">
					<tr>
						<th class="px-4 py-2 text-center">rank_</th>
						<th class="px-4 py-2 text-center">team_name_</th>
						<th class="px-4 py-2 text-center">score_</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(item, index) in scoreboard" :key="index" :class="index % 2 != 0 ? 'bg-[#2a2a2a] text-white' : ''">
						<td class="px-4 py-2 text-center">{{ index + 1 }}</td>
						<td class="px-4 py-2 text-center">{{ item.name }}</td>
						<td class="px-4 py-2 text-center">{{ item.score }}</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted, onUnmounted } from "vue"
	import { useAppStore } from "../stores/appStore"

	const appStore = useAppStore()
	const scoreboard = ref([])
	const tableContainer = ref(null)
	let reverseScroll = false
	let intervalId
	const scrollSpeed = 1
	const scrollRefreshRate = 35
	let waitUntil

	const convertObjectToArray = (obj) => {
		return Object.keys(obj).map((key) => ({
			...obj[key],
			rank: parseInt(key),
		}))
	}

	function scrollTable() {
		if (waitUntil && Date.now() < waitUntil) return
		const scrollPos = tableContainer.value.scrollTop + tableContainer.value.clientHeight
		console.log(tableContainer.value.clientHeight, tableContainer.value.scrollHeight)
		console.log(scrollPos)

		if (scrollPos >= tableContainer.value.scrollHeight) {
			reverseScroll = true
			waitUntil = Date.now() + 2000
		} else if (reverseScroll && tableContainer.value.scrollTop <= 0) {
			reverseScroll = false
			waitUntil = Date.now() + 5000
			return
		}

		if (reverseScroll) tableContainer.value.scrollTop -= scrollSpeed
		else tableContainer.value.scrollTop += scrollSpeed
	}

	onMounted(() => {
		appStore.socket.on("new-flag", (data) => {
			scoreboard.value = convertObjectToArray(data.scoreboard)
		})

		intervalId = setInterval(scrollTable, scrollRefreshRate)
	})

	onUnmounted(() => {
		clearInterval(intervalId)
	})
</script>

<style scoped>
	.no-scrollbar::-webkit-scrollbar {
		display: none;
	}

	.no-scrollbar {
		-ms-overflow-style: none; /* Internet Explorer 10+ */
		scrollbar-width: none; /* Firefox */
	}
</style>
