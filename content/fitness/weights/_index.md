---
title: "Weights"
toc: false
showreadingtime: false
layout: single
---

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  .terminal-nav { display: none; }

  .gym-h1 { font-weight: bold; font-size: 1.5em; margin: 0 0 0.2em 0; color: #000; }
  .gym-sub { color: #888; font-size: 0.9em; margin: 0 0 2em 0; }
  .gym-h2 { font-weight: bold; font-size: 1em; margin: 2em 0 0.7em 0; color: #000; }

  /* The week: a coloured tick over each day, no boxes. Colours match the
     heatmap on /fitness so a ride is the same orange everywhere. */
  .week { display: grid; grid-template-columns: repeat(7, 1fr); gap: 0 0.9em; }
  @media (max-width: 560px) { .week { grid-template-columns: repeat(4, 1fr); gap: 1em 0.8em; } }
  .day .bar { height: 2px; border-radius: 1px; background: #e5e0d5; }
  .day .in { padding: 0.45em 0 0; }
  .day .d { font-size: 0.66em; letter-spacing: 0.05em; text-transform: uppercase; color: #a9a094; }
  .day .a { font-size: 0.85em; margin-top: 0.2em; color: #000; }
  .day.rest .a { color: #c3bbac; }
  .lift .bar { background: #699bd3; }
  .run  .bar { background: #61b885; }
  .ride .bar { background: #f6a351; }
  .rest .bar { background: #e5e0d5; }

  .week-head { display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.4em 1em; margin: 2em 0 0.7em; }
  .week-head .gym-h2 { margin: 0; }
  .legend { display: flex; flex-wrap: wrap; gap: 0.9em; font-size: 0.75em; color: #888; }
  .legend span { display: inline-flex; align-items: center; gap: 0.45em; }
  .legend .sw { width: 14px; height: 4px; border-radius: 2px; display: inline-block; }

  /* lift cards */
  .lifts { display: grid; grid-template-columns: 1fr 1fr; gap: 1.6em 2.4em; }
  @media (max-width: 560px) { .lifts { grid-template-columns: 1fr; } }
  .card .h { font-weight: bold; color: #000; margin: 0 0 0.4em 0; font-size: 0.95em; }
  /* The lift and its reps are what you read mid-session, so they are the
     largest thing here; the swap-in and the notes are reference and sit back. */
  table.ex { width: 100%; border-collapse: collapse; font-size: 1.05em; }
  table.ex td { padding: 0.55em 0; border-bottom: 1px solid #f2efe8; vertical-align: baseline; }
  table.ex td:first-child { width: 100%; color: #000; }
  table.ex tr:last-child td { border-bottom: none; }
  table.ex td.r { text-align: right; color: #000; font-weight: bold; white-space: nowrap;
                  font-variant-numeric: tabular-nums; padding-left: 1.2em; }
  .alt { display: block; font-size: 0.72em; color: #b3ab9a; margin-top: 0.15em; }
  .alt .sw { color: #c9c2b4; margin-right: 0.3em; }

  /* The progression rule reads as a plain sentence; a tinted box made the one
     thing you actually need to remember look like boilerplate. */
  .callout { font-size: 0.85em; color: #6b6459; margin: 0 0 0.9em 0; line-height: 1.6; }
  .callout b { color: #000; }

  .rules .rule { display: grid; grid-template-columns: 5.5em 1fr; gap: 0.9em; padding: 0.5em 0; border-bottom: 1px solid #f2efe8; font-size: 0.8em; }
  .rules .rule:last-child { border-bottom: none; }
  .rules .k { font-weight: bold; color: #000; }
  .rules .v { color: #6b6459; line-height: 1.5; }

  .note { display:block; color:#a9a094; font-size:0.75em; line-height:1.55; border-left: 2px solid #E5DECF; padding-left: 0.6em; margin: 0.55em 0; }
  .src { margin-top: 2.4em; }
</style>

<p class="gym-sub">Two lifts, two runs, one ride a week.</p>

<div class="week-head">
<p class="gym-h2">The week</p>
<div class="legend"><span><span class="sw" style="background:#61b885"></span>Run</span><span><span class="sw" style="background:#699bd3"></span>Lift</span><span><span class="sw" style="background:#f6a351"></span>Ride</span><span><span class="sw" style="background:#e5e0d5"></span>Rest</span></div>
</div>
<div class="week">
<div class="day run"><div class="bar"></div><div class="in"><div class="d">Mon</div><div class="a">Run</div></div></div>
<div class="day lift"><div class="bar"></div><div class="in"><div class="d">Tue</div><div class="a">Lift A</div></div></div>
<div class="day run"><div class="bar"></div><div class="in"><div class="d">Wed</div><div class="a">Run</div></div></div>
<div class="day lift"><div class="bar"></div><div class="in"><div class="d">Thu</div><div class="a">Lift B</div></div></div>
<div class="day rest"><div class="bar"></div><div class="in"><div class="d">Fri</div><div class="a">Rest</div></div></div>
<div class="day ride"><div class="bar"></div><div class="in"><div class="d">Sat</div><div class="a">Ride</div></div></div>
<div class="day rest"><div class="bar"></div><div class="in"><div class="d">Sun</div><div class="a">Rest</div></div></div>
</div>
<span class="note">Runs at lunch, ride is 100k. Move days to fit work, rest either side of the ride.</span>

<p class="gym-h2">The lifts</p>
<div class="lifts">
<div class="card">
<p class="h">Lift A</p>
<table class="ex">
<tr><td>Squat<span class="alt"><span class="sw">⇄</span>or Front squat, easier on the back</span></td><td class="r">3 x 8</td></tr>
<tr><td>Bench press</td><td class="r">3 x 8</td></tr>
<tr><td><a href="https://www.youtube.com/shorts/Nqh7q3zDCoQ" target="_blank" rel="noopener">Barbell row</a></td><td class="r">3 x 8</td></tr>
<tr><td>Dips</td><td class="r">3 x max</td></tr>
</table>
</div>
<div class="card">
<p class="h">Lift B</p>
<table class="ex">
<tr><td><a href="https://www.youtube.com/shorts/4LBVP2Oe7fg" target="_blank" rel="noopener">Overhead press</a><span class="alt"><span class="sw">⇄</span>or Push press, more weight</span></td><td class="r">3 x 8</td></tr>
<tr><td><a href="https://www.youtube.com/shorts/xNwpvDuZJ3k" target="_blank" rel="noopener">Deadlift</a><span class="alt"><span class="sw">⇄</span>or <a href="https://www.youtube.com/shorts/5rIqP63yWFg" target="_blank" rel="noopener">Romanian deadlift</a>, easier on the back</span></td><td class="r">3 x 5</td></tr>
<tr><td><a href="https://www.youtube.com/shorts/phVtqawIgbk" target="_blank" rel="noopener">Barbell row</a></td><td class="r">3 x 8</td></tr>
<tr><td>Dips</td><td class="r">3 x max</td></tr>
</table>
</div>
</div>
<span class="note">Dips stop a couple short of failure. Everything else is the same weight across all sets.</span>
<span class="note">⇄ is a swap-in when the main lift does not suit the day.</span>

<p class="gym-h2">How it works</p>
<div class="callout"><b>Hit every rep, add weight next time.</b> 2.5kg on the bar lifts, 5kg on the deadlift. Miss reps and stay at the same weight until you get them.</div>
<div class="card rules">
<div class="rule"><span class="k">Rest</span><span class="v">2 to 3 minutes between heavy sets. Warm up with two lighter sets.</span></div>
<div class="rule"><span class="k">Legs</span><span class="v">Squat one day, deadlift the other. Never both heavy.</span></div>
<div class="rule"><span class="k">Back</span><span class="v">Rows stand in for pull-ups. Add chin-ups once you get the bar.</span></div>
<div class="rule"><span class="k">Recovery</span><span class="v">No heavy legs the day before a ride.</span></div>
</div>

<span class="note src">Sources: <a href="https://thefitness.wiki/routines/r-fitness-basic-beginner-routine/">r/Fitness Basic Beginner Routine</a>, <a href="https://www.strengthlog.com/strength-training-for-cyclists/">StrengthLog</a>, <a href="https://www.simongpt.co.uk/pt-strength-and-conditioning-coach-for-cyclists-and-endurance-athletes/">simongPT</a>.</span>
