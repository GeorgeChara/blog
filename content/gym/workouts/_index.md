---
title: "Workouts"
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

  /* week grid */
  .week { display: grid; grid-template-columns: repeat(7, 1fr); gap: 0.4em; }
  @media (max-width: 560px) { .week { grid-template-columns: repeat(3, 1fr); } }
  .day { border: 1px solid #eee; border-radius: 4px; overflow: hidden; }
  .day .bar { height: 4px; background: #d8d8d8; }
  .day .in { padding: 0.5em 0.6em; }
  .day .d { font-size: 0.7em; letter-spacing: 0.05em; text-transform: uppercase; color: #aaa; }
  .day .a { font-size: 0.85em; margin-top: 0.25em; }
  .day.rest .a { color: #bbb; }
  .lift .bar { background: #4169E1; }
  .run  .bar { background: #3aa06a; }
  .ride .bar { background: #d98a2b; }
  .rest .bar { background: #d8d8d8; }

  .week-head { display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.4em 1em; margin: 2em 0 0.7em; }
  .week-head .gym-h2 { margin: 0; }
  .legend { display: flex; flex-wrap: wrap; gap: 0.9em; font-size: 0.75em; color: #888; }
  .legend span { display: inline-flex; align-items: center; gap: 0.45em; }
  .legend .sw { width: 14px; height: 4px; border-radius: 2px; display: inline-block; }

  /* lift cards */
  .lifts { display: grid; grid-template-columns: 1fr 1fr; gap: 1em; }
  @media (max-width: 560px) { .lifts { grid-template-columns: 1fr; } }
  .card { border: 1px solid #e5decf; border-radius: 4px; padding: 0.9em 1.1em; }
  .card .h { font-weight: bold; color: #000; margin: 0 0 0.5em 0; font-size: 0.95em; }
  table.ex { width: 100%; border-collapse: collapse; font-size: 0.9em; }
  table.ex td { padding: 0.4em 0; border-bottom: 1px solid #f2efe8; }
  table.ex td:first-child { width: 100%; }
  table.ex tr:last-child td { border-bottom: none; }
  table.ex td.r { text-align: left; color: #666; white-space: nowrap; font-variant-numeric: tabular-nums; }

  /* callout */
  .callout { border-left: 3px solid #4169E1; background: #f3f6fd; border-radius: 0 4px 4px 0; padding: 0.7em 0.9em; font-size: 0.85em; color: #333; margin: 0 0 0.8em 0; }
  .callout b { color: #000; }

  .rules .rule { display: grid; grid-template-columns: 6em 1fr; gap: 0.8em; padding: 0.55em 0; border-bottom: 1px solid #f2efe8; font-size: 0.85em; }
  .rules .rule:last-child { border-bottom: none; }
  .rules .k { font-weight: bold; color: #000; }
  .rules .v { color: #555; line-height: 1.5; }

  .note { display:block; color:#888; font-size:0.8em; line-height:1.6; border-left: 2px solid #E5DECF; padding-left: 0.6em; margin: 0.55em 0; }
  .src { margin-top: 2.4em; }
</style>

<p class="gym-h1">Workouts</p>
<p class="gym-sub">Two lifts, two runs, one ride a week.</p>

<div class="week-head">
<p class="gym-h2">The week</p>
<div class="legend"><span><span class="sw" style="background:#3aa06a"></span>Run</span><span><span class="sw" style="background:#4169E1"></span>Lift</span><span><span class="sw" style="background:#d98a2b"></span>Ride</span><span><span class="sw" style="background:#d8d8d8"></span>Rest</span></div>
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
<span class="note">Runs at lunch, ride is 100k. Move the days around to fit work, and keep a rest day either side of the ride.</span>

<p class="gym-h2">The lifts</p>
<div class="lifts">
<div class="card">
<p class="h">Lift A</p>
<table class="ex">
<tr><td>Bench press</td><td class="r">3 x 5</td></tr>
<tr><td><a href="https://www.youtube.com/shorts/Nqh7q3zDCoQ" target="_blank" rel="noopener">Barbell row</a></td><td class="r">3 x 5</td></tr>
<tr><td><a href="https://www.youtube.com/shorts/5rIqP63yWFg" target="_blank" rel="noopener">Romanian deadlift</a></td><td class="r">3 x 8</td></tr>
<tr><td>Dips</td><td class="r">3 x max</td></tr>
</table>
</div>
<div class="card">
<p class="h">Lift B</p>
<table class="ex">
<tr><td><a href="https://www.youtube.com/shorts/4LBVP2Oe7fg" target="_blank" rel="noopener">Overhead press</a></td><td class="r">3 x 5</td></tr>
<tr><td><a href="https://www.youtube.com/shorts/xNwpvDuZJ3k" target="_blank" rel="noopener">Deadlift</a></td><td class="r">3 x 5</td></tr>
<tr><td><a href="https://www.youtube.com/shorts/phVtqawIgbk" target="_blank" rel="noopener">Barbell row</a></td><td class="r">3 x 5</td></tr>
<tr><td>Dips</td><td class="r">3 x max</td></tr>
</table>
</div>
</div>
<span class="note">Dips to a couple short of failure. Everything else is a straight weight across all sets.</span>

<p class="gym-h2">How it works</p>
<div class="callout"><b>Hit every rep, add weight next time.</b> 2.5kg on the bar lifts, 5kg on the deadlift. Miss reps and stay at the same weight until you get them.</div>
<div class="card rules">
<div class="rule"><span class="k">Rest</span><span class="v">2 to 3 minutes between the heavy sets. Warm up each lift with a couple of lighter sets first.</span></div>
<div class="rule"><span class="k">Legs</span><span class="v">No squat rack, so they come from the deadlifts, the bike and the runs. Plenty for a lean, athletic build.</span></div>
<div class="rule"><span class="k">Back</span><span class="v">Rows on both days stand in for pull-ups. Add chin-ups once you get the bar.</span></div>
<div class="rule"><span class="k">Recovery</span><span class="v">Keep the heavy deadlift day away from the day before your ride.</span></div>
</div>

<span class="note src">Sources: <a href="https://thefitness.wiki/routines/r-fitness-basic-beginner-routine/">r/Fitness Basic Beginner Routine</a>, <a href="https://www.strengthlog.com/strength-training-for-cyclists/">StrengthLog</a>, <a href="https://www.simongpt.co.uk/pt-strength-and-conditioning-coach-for-cyclists-and-endurance-athletes/">simongPT</a>.</span>
