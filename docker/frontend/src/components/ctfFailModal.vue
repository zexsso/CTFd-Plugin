<template>
	<transition name="modal" v-show="visible">
		<div class="absolute inset-0 z-50">
			<div class="absolute inset-0 backdrop-blur-sm"></div>
			<div
				class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-lg border bg-zinc-900 px-4"
			>
				<div class="w-[50vw] m-4">
					<div class="flex justify-between">
						<div class="flex space-x-2">
							<p class="font-bold">Challenge:</p>
							<p>{{ props.content.challenge }}</p>
						</div>
						<div class="flex space-x-2">
							<p class="font-bold">Team:</p>
							<p>{{ props.content.team }}</p>
						</div>
					</div>
                    <h1 class="text-xl text-center mt-2">{{ props.content.user }} {{ eventText }} {{ props.content.challenge }}</h1>
                    <div class="flex justify-between">
                        <div class="flex space-x-2">
							<p class="font-bold">Team rank:</p>
							<p>{{ props.content.team_rank }}</p>
						</div>
						<div class="flex space-x-2">
							<p class="font-bold">User solves:</p>
							<p>{{ props.content.user_solves }}</p>
						</div>
                    </div>
				</div>
			</div>
		</div>
	</transition>
</template>

<script setup>
	import { ref, onMounted } from "vue"
	import { useAppStore } from "@/stores/appStore"

	const appStore = useAppStore()
	const visible = ref(false)
	const props = defineProps({
		content: {
			type: Object, // Utilisez le type approprié selon vos besoins
			required: true,
		},
	})
	const eventText = ref("")

	onMounted(() => {
		setTimeout(() => {
			visible.value = true
		}, 100)
	})
</script>

<style scoped>
	.modal-enter-active,
	.modal-leave-active {
		transition: opacity 0.2s linear, transform 0.2s linear;
	}

	.modal-enter-from,
	.modal-leave-to {
		opacity: 0;
		transform: scale(0.9);
	}

	.modal-content {
		transition: transform 0.2s linear, opacity 0.2s linear;
	}
</style>
