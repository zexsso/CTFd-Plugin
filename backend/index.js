import express from "express"
import { createServer } from "node:http"
import { Server } from "socket.io"
import bodyParser from "body-parser"
import cors from "cors"
import http from "http"

const app = express()
const server = createServer(app)
const io = new Server(server)

// Middleware pour analyser le corps des requêtes entrantes
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

// Middleware pour permettre les CORS (Cross-Origin Resource Sharing)
app.use(cors())

// Endpoint pour recevoir les webhooks
app.post("/webhook", (req, res) => {
	const payload = req.body
	console.log("Webhook received:", payload)

	// verify scroboard is good
	io.emit("new-flag", payload)

	res.status(200).send("Webhook received")
})

io.on("connection", (socket) => {
	console.log(socket.id + " connected")

	socket.on("disconnect", () => {
		console.log(socket.id + " disconnected")
	})
})

server.listen(3000, async () => {
	console.log("server running at http://localhost:3000")
	http.get({ host: "ifconfig.me", port: 80, path: "/" }, (resp) => {
		resp.on("data", (ip) => console.log("server running at: http://" + ip + ":3000"))
	})
})
