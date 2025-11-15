const app = require("./app");
const express = require("express");
require("dotenv").config();
const cors = require("cors");
const path = require("path");
const { PythonShell } = require("python-shell");

// Middleware
app.use(cors()); // Enable CORS for frontend requests
app.use(express.static(path.join(__dirname, "public"))); // Serve dashboard.html

// Prediction endpoint
app.post("/predict", async (req, res) => {
  const { dateTime, irradiation, ambientTemp, moduleTemp } = req.body;

  // Validate inputs
  if (!dateTime || irradiation == null || ambientTemp == null || moduleTemp == null) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  // Prepare data for Python script
  const inputData = {
    dateTime,
    irradiation: parseFloat(irradiation),
    ambientTemp: parseFloat(ambientTemp),
    moduleTemp: parseFloat(moduleTemp)
  };

  // Configure PythonShell
  const options = {
    mode: "text",
    pythonOptions: ["-u"], // Unbuffered output
    scriptPath: __dirname,
    args: [JSON.stringify(inputData)]
  };

  try {
    // Run Python script
    const results = await new Promise((resolve, reject) => {
      PythonShell.run("predict.py", options, (err, output) => {
        if (err) return reject(err);
        try {
          const result = JSON.parse(output[0]);
          resolve(result);
        } catch (parseErr) {
          reject(new Error("Failed to parse Python output"));
        }
      });
    });

    if (results.error) {
      return res.status(400).json({ error: results.error });
    }

    res.json(results);
  } catch (error) {
    console.error("Prediction error:", error);
    res.status(500).json({ error: "Prediction failed: " + error.message });
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`EnergyChain backend running on PORT ${PORT}`);
});