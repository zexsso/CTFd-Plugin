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

// Server variables
let lastUpdate = null
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
app.post("/", (req, res) => {
	lastUpdate = req.body
	io.emit("new-flag", req.body)
	res.status(200).send("Webhook received")
	writeToFile(req.body)
})

app.post("/incorrect", (req, res) => {
	// lastUpdate = req.body
	// update fail
	console.log(req.body)
	io.emit("new-fail", req.body)
	res.status(200).send("Webhook received")
	// writeToFile(req.body)
})

io.on("connection", (socket) => {
	console.log(socket.id + " connected")

	if (lastUpdate == null) lastUpdate = readFromFile()
	socket.emit("new-flag", lastUpdate)

	socket.on("disconnect", () => console.log(socket.id + " disconnected"))
})

server.listen(3000, () => {
	console.log("server running at http://localhost:3000")
	http.get({ host: "ifconfig.me", port: 80, path: "/" }, (resp) => {
		resp.on("data", (ip) => console.log("server running at: http://" + ip + ":3000"))
	})
})
