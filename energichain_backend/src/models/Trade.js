const { DataTypes } = require("sequelize");
const sequelize = require("../config/db");

const Trade = sequelize.define("Trade", {
  id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
  userId: { type: DataTypes.INTEGER },
  energyUnits: { type: DataTypes.FLOAT },
  pricePerUnit: { type: DataTypes.FLOAT },
  tradeType: { type: DataTypes.STRING }, // "buy" or "sell"
});

module.exports = Trade;
