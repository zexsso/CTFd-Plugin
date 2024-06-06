import { defineStore } from "pinia"
import { ref } from "vue"
import { io } from "socket.io-client"

export const useAppStore = defineStore("app", () => {
	// Vue & PrimeVue
	const toast = ref()
	const socket = ref()

	function connectSocket() {
		socket.value = io(`${import.meta.env.VITE_SOCKET_URL}`, { transports: ["websocket"] })
		socket.value.on("connect", () => {
			console.log("Connected to the socket server")
		})
		
		socket.value.on("new-flag", (data) => {
			console.log("newFlag")
			console.log(data)
		})

		socket.value.on("disconnect", () => {
			console.log("Disconnected from the socket server")
		})
	}

	return {
		toast,
		socket,
		connectSocket,
	}
})
