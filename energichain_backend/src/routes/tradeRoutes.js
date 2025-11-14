const express = require("express");
const router = express.Router();

const auth = require("../middleware/authMiddleware");
const { createTrade, getMyTrades } = require("../controllers/tradeController");

router.post("/create", auth, createTrade);
router.get("/mine", auth, getMyTrades);

module.exports = router;
