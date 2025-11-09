# ELECTROHACK
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Concise — Review Summarizer</title>
  <style>
    body {
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      background: #f6f8fb;
      color: #111827;
      margin: 0;
      padding: 2rem;
      display: flex;
      justify-content: center;
    }
    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 6px 18px rgba(15,23,42,0.08);
      max-width: 820px;
      width: 100%;
      padding: 28px;
    }
    h1 {
      margin: 0 0 8px 0;
      font-size: 1.6rem;
    }
    p.lead {
      margin: 0 0 18px 0;
      line-height: 1.6;
      color: #374151;
    }
    ul.features {
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      gap: 8px;
    }
    ul.features li {
      padding: 10px 12px;
      border-radius: 8px;
      background: #f1f5f9;
      display: flex;
      gap: 12px;
      align-items: center;
      color: #0f172a;
    }
    .dot {
      min-width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #2563eb;
      display: inline-block;
    }
    footer {
      margin-top: 18px;
      font-size: 0.9rem;
      color: #6b7280;
    }
  </style>
</head>
<body>
  <article class="card" aria-labelledby="title">
    <header>
      <h1 id="title">Concise — AI-powered Review Summarizer</h1>
      <p class="lead">
        Concise is a web-based NLP application that helps online buyers make smarter purchase decisions by automatically analyzing and summarizing product reviews.
        Given a product link, the system fetches all reviews, performs sentiment analysis, extracts keywords, and generates concise pros and cons along with an overall summary score.
      </p>
    </header>

    <section aria-labelledby="features">
      <h2 id="features" style="font-size:1rem;margin:0 0 8px 0;">Key Features</h2>
      <ul class="features">
        <li><span class="dot" aria-hidden="true"></span>Automatic review fetching from product pages</li>
        <li><span class="dot" aria-hidden="true"></span>Per-review sentiment analysis (positive / negative / neutral)</li>
        <li><span class="dot" aria-hidden="true"></span>Keyword extraction to highlight common themes</li>
        <li><span class="dot" aria-hidden="true"></span>Generates concise Pros &amp; Cons summary</li>
        <li><span class="dot" aria-hidden="true"></span>Provides an overall summary score for quick decision-making</li>
      </ul>
    </section>

    <footer>
      Tip: Paste a product URL into Concise to get a summarized report of user sentiment and the most-cited pros &amp; cons.
    </footer>
  </article>
</body>
</html>
