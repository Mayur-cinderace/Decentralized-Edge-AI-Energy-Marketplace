const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const { User } = require("../models");

exports.signup = async (req, res) => {
  try {
    const { name, email, password } = req.body;

    // Validate input BEFORE hashing
    if (!name || !email || !password) {
      return res.status(400).json({ msg: "All fields are required" });
    }

    // Check if user already exists
    const existingUser = await User.findOne({ where: { email } });
    if (existingUser) {
      return res.status(400).json({ msg: "User already exists" });
    }

    // Hash password
    const hashed = await bcrypt.hash(password, 10);

    // Create user
    const user = await User.create({
      name,
      email,
      password: hashed
    });

    res.status(201).json({ 
      msg: "User created successfully", 
      user: {
        id: user.id,
        name: user.name,
        email: user.email
      }
    });
  } catch (error) {
    console.error("Signup error:", error);
    res.status(500).json({ msg: "Server error during signup" });
  }
};

exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;

    // Validate input
    if (!email || !password) {
      return res.status(400).json({ msg: "Email and password are required" });
    }

    // Find user
    const user = await User.findOne({ where: { email } });
    if (!user) {
      return res.status(404).json({ msg: "User not found" });
    }

    // Check password
    const match = await bcrypt.compare(password, user.password);
    if (!match) {
      return res.status(400).json({ msg: "Incorrect password" });
    }

    // Generate token
    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, {
      expiresIn: '24h'
    });

    res.json({
      msg: "Login successful",
      token,
      user: {
        id: user.id,
        name: user.name,
        email: user.email
      }
    });
  } catch (error) {
    console.error("Login error:", error);
    res.status(500).json({ msg: "Server error during login" });
  }
};