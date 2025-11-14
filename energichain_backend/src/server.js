const app = require("./app");
const { connectDB } = require("./models");
require("dotenv").config();

const PORT = process.env.PORT || 5000;

connectDB();

app.listen(PORT, () => {
  console.log(`EnergyChain backend running on PORT ${PORT}`);
});
