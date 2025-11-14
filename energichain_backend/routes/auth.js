// routes/auth.js
router.post('/signup', async (req, res) => {
  const { name, email, password } = req.body;

  // 1. validation (omitted for brevity)
  // 2. hash password
  const hashed = await bcrypt.hash(password, 10);

  // 3. save user
  const user = await User.create({ name, email, password: hashed });

  // 4. **create JWT** (so the user is logged-in immediately)
  const token = jwt.sign({ id: user._id, email: user.email }, process.env.JWT_SECRET, {
    expiresIn: '7d',
  });

  res.json({
    token,
    user: { name: user.name, email: user.email },
    msg: 'Signup successful',
  });
});