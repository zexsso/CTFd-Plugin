import express from "express"
import { createServer } from "node:http"
import { Server } from "socket.io"
import bodyParser from "body-parser"
import cors from "cors"
import http from "http"
import fs from "fs"

const app = express()
const server = createServer(app)
const io = new Server(server)

// Middleware for parsing JSON and urlencoded data
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(cors())
let numberOfClients = 0

// Server variables
let lastUpdate = undefined
const cacheFilePath = "lastUpdate.json"

function writeToFile(data) {
	fs.writeFileSync(cacheFilePath, JSON.stringify(data, null, 2), "utf8")
}

function readFromFile() {
	if (fs.existsSync(cacheFilePath)) {
		const data = fs.readFileSync(cacheFilePath, "utf8")
		return JSON.parse(data)
	}
}

// Endpoint for receiving webhook data
app.post("/webhook", (req, res) => {
	lastUpdate = req.body
	io.emit("new-flag", req.body)
	res.status(200).send("Webhook received")
	writeToFile(req.body)
})

app.post("/webhook/incorrect", (req, res) => {
	io.emit("new-fail", req.body)
	res.status(200).send("Webhook received")
})

io.on("connection", (socket) => {
	++numberOfClients
	console.log(socket.id, "connected", numberOfClients, "clients")

	if (!lastUpdate) lastUpdate = readFromFile()
	if (lastUpdate) socket.emit("new-flag", lastUpdate)

	socket.on("disconnect", () => {
		--numberOfClients
		console.log(socket.id, "disconnected", numberOfClients, "clients")
	})
})

server.listen(3000, () => {
	console.log("server running at http://localhost:3000")
	http.get({ host: "ifconfig.me", port: 80, path: "/" }, (resp) => {
		resp.on("data", (ip) => console.log("server running at: http://" + ip + ":3000"))
	})
})
