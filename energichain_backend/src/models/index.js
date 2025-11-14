const sequelize = require("../config/db");
const User = require("./User");
const Trade = require("./Trade");

// associations
User.hasMany(Trade, { foreignKey: "userId" });
Trade.belongsTo(User, { foreignKey: "userId" });

const connectDB = async () => {
  try {
    await sequelize.sync({ alter: true });
    console.log("Postgres DB synced!");
  } catch (err) {
    console.error("DB Connection Error:", err);
  }
};

module.exports = { sequelize, User, Trade, connectDB };
