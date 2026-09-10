// Minimal Node.js server for GoDaddy's "Setup Node.js App" hosting.
// Serves the pre-built static site (HTML/CSS/JS) exactly as a plain
// static host would — no templating, no database.
const express = require('express');
const path = require('path');

const app = express();

// GoDaddy's Node.js hosting sets PORT for you; fall back to 3000 locally.
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname), {
  extensions: ['html'],
}));

// Friendly 404 that still matches the site's look would need a template;
// keep this simple since the site has no client-side router.
app.use((req, res) => {
  res.status(404).sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Wellforge site listening on port ${PORT}`);
});
