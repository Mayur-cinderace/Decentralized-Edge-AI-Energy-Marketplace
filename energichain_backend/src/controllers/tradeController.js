const { Trade } = require("../models");

exports.createTrade = async (req, res) => {
  const { energyUnits, pricePerUnit, tradeType } = req.body;

  const trade = await Trade.create({
    userId: req.user.id,
    energyUnits,
    pricePerUnit,
    tradeType,
  });

  res.json({ msg: "Trade recorded", trade });
};

exports.getMyTrades = async (req, res) => {
  const trades = await Trade.findAll({ where: { userId: req.user.id } });

  res.json(trades);
};
