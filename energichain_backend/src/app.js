const express = require("express");
const cors = require("cors");

const authRoutes = require("./routes/authRoutes");
const tradeRoutes = require("./routes/tradeRoutes");

const app = express();

app.use(cors());
app.use(express.json());

// serve your landing page
app.use(express.static("public")); // put your HTML here

app.use("/auth", authRoutes);
app.use("/trade", tradeRoutes);

module.exports = app;
