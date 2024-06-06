<template>
	<div class="flex justify-center h-[60vh] w-full">
		<DataTable :value="products" stripedRows sortField="Score" :sortOrder="-1" class="w-[80vw] p-10">
			<Column field="Place" header="Place"></Column>
			<Column field="Equipe" header="Equipe"></Column>
			<Column field="Score" header="Score" :sortable="true"></Column>
			<Column field="NombreChallengesValides" header="Nombre de Challenges Validés"></Column>
		</DataTable>
	</div>
</template>

<script setup>
	import { ref, onMounted } from "vue"


	let data = [
		{ Equipe: "Byting Wolves", Score: 2000, NombreChallengesValides: 1 },
		{ Equipe: "Code Crusaders", Score: 950, NombreChallengesValides: 9 },
		{ Equipe: "Debugging Ninjas", Score: 900, NombreChallengesValides: 8 },
		{ Equipe: "Syntax Sorcerers", Score: 850, NombreChallengesValides: 7 },
		{ Equipe: "Binary Beasts", Score: 800, NombreChallengesValides: 6 },
		{ Equipe: "Compiling Wizards", Score: 750, NombreChallengesValides: 5 },
		{ Equipe: "Algorithm Avengers", Score: 700, NombreChallengesValides: 4 },
		{ Equipe: "Pseudocode Pirates", Score: 650, NombreChallengesValides: 3 },
		{ Equipe: "Programming Pioneers", Score: 600, NombreChallengesValides: 2 },
		{ Equipe: "Data Divas", Score: 550, NombreChallengesValides: 1 },
		{ Equipe: "Compiling Wizards", Score: 750, NombreChallengesValides: 5 },
		{ Equipe: "Algorithm Avengers", Score: 700, NombreChallengesValides: 4 },
		{ Equipe: "Pseudocode Pirates", Score: 650, NombreChallengesValides: 3 },
		{ Equipe: "Programming Pioneers", Score: 600, NombreChallengesValides: 2 },
		{ Equipe: "Data Divas", Score: 550, NombreChallengesValides: 1 },
	]

	const products = ref([])

	const chartData = ref()
	const chartOptions = ref()

	const maxTeam = 10

	onMounted(() => {
		chartData.value = setChartData()
		chartOptions.value = setChartOptions()

		// Sort the data array by Score in descending order
		data.sort((a, b) => b.Score - a.Score)

		// Limiter à 10 équipes
		const limitedData = data.slice(0, maxTeam)

		// Assign dynamic Place values
		data = limitedData.map((item, index) => {
			return {
				...item,
				Place: index + 1,
			}
		})

		products.value = data
	})

	const setChartData = () => {
		const documentStyle = getComputedStyle(document.documentElement)

		return {
			labels: ["January", "February", "March", "April", "May", "June", "July"],
			datasets: [
				{
					label: "First Dataset",
					data: [0, 69, 80, 81, 96, 155, 240],
					fill: false,
					borderColor: documentStyle.getPropertyValue("--cyan-500"),
					tension: 0.4,
				},
				{
					label: "Second Dataset",
					data: [0, 38, 40, 59, 86, 97, 150],
					fill: false,
					borderColor: documentStyle.getPropertyValue("--gray-500"),
					tension: 0.4,
				},
				{
					label: "Third Dataset",
					data: [0, 47, 57, 67, 87, 97, 107],
					fill: false,
					borderColor: documentStyle.getPropertyValue("--red-500"),
					tension: 0.4,
				},
			],
		}
	}

	const setChartOptions = () => {
		const documentStyle = getComputedStyle(document.documentElement)
		const textColor = documentStyle.getPropertyValue("--text-color")
		const textColorSecondary = documentStyle.getPropertyValue("--text-color-secondary")
		const surfaceBorder = documentStyle.getPropertyValue("--surface-border")

		return {
			maintainAspectRatio: false,
			aspectRatio: 0.6,
			plugins: {
				legend: {
					labels: {
						color: textColor,
					},
				},
			},
			scales: {
				x: {
					ticks: {
						color: textColorSecondary,
					},
					grid: {
						color: surfaceBorder,
					},
				},
				y: {
					ticks: {
						color: textColorSecondary,
					},
					grid: {
						color: surfaceBorder,
					},
				},
			},
		}
	}
</script>
