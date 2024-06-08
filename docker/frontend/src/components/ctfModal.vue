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
				<p class="text-[#20C20E]">{{ props.content.challenge }}</p>
			  </div>
			  <div class="flex space-x-2">
				<p class="font-bold">Team:</p>
				<p class="text-[#20C20E]">{{ props.content.team }}</p>
			  </div>
			</div>
			<h1 class="text-xl text-center mt-2">
			  {{ props.content.user }} {{ eventText }} {{ props.content.challenge }}
			</h1>
			<div class="flex justify-center p-4">
			  <img v-if="flagType == 'category_complete'" src="@/assets/gifs/category_complete.gif" alt="" />
			  <img v-if="flagType == 'defuse_bomb'" src="@/assets/gifs/defuse_bomb.gif" alt="" />
			  <img v-if="flagType == 'first_blood'" src="@/assets/gifs/first_blood.gif" alt="" />
			  <img v-if="flagType == 'solved'" src="@/assets/gifs/solved.gif" alt="" />
			</div>
			<div class="flex justify-between">
			  <div class="flex space-x-2">
				<p class="font-bold">Team rank:</p>
				<p class="text-[#20C20E]">{{ props.content.team_rank }}</p>
			  </div>
			  <div class="flex space-x-2">
				<p class="font-bold">User solves:</p>
				<p class="text-[#20C20E]">{{ props.content.user_solves }}</p>
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
		type: Object,
		required: true,
	  },
	})
	const eventText = ref("")
	const flagType = ref("") 
  
	onMounted(() => {
	  if (props.content.is_category_complete == true) {
		eventText.value = "complete the category of the challenge"
		flagType.value = "category_complete"
	  } else if (props.content.challenge == "") {
		eventText.value = "defuse the challenge"
		flagType.value = "defuse_bomb"
	  } else if (props.content.solve_id == 0) {
		eventText.value = "first_blood the challenge"
		flagType.value = "first_blood"
	  } else if (props.content.solve_id > 0) {
		eventText.value = "solved the challenge"
		flagType.value = "solved"
	  } else {
		eventText.value = "solved"
		flagType.value = "solved"
		console.log("bizarre")
	  }
  
	  setTimeout(() => {
		visible.value = true;
	  }, 100);
	});
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
  