// Render <project>/scene.html frame by frame with system Chrome, pipe JPEG frames into ffmpeg.
//
// Usage:
//   PLAYWRIGHT_MODULE=<path/to/node_modules/playwright> node render.js --project <dir> [--stills 3,6.5,10] [--fps 30]
//
// Scene contract: window.setup(timeline) once, then window.render(t) draws frame t (seconds) onto <canvas id="c">.
// render(t) must be a pure function of t: no timers, Date.now, requestAnimationFrame, or unseeded Math.random.

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[flow_coding_vedio/render] ${msg}`);
  process.exit(1);
}

function parseArgs(argv) {
  const out = { fps: 30, stills: null, project: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--project') out.project = argv[++i];
    else if (a === '--stills') out.stills = (argv[++i] || '').split(',').map(Number);
    else if (a === '--fps') out.fps = Number(argv[++i]);
    else fail(`unknown arg: ${a}\n  Expected: --project <dir> [--stills t1,t2] [--fps 30]`);
  }
  if (!out.project) fail('missing --project <dir>');
  if (!Number.isFinite(out.fps) || out.fps <= 0) fail(`--fps must be a positive number\n  Actual: ${out.fps}`);
  if (out.stills && (out.stills.length === 0 || out.stills.some((n) => !Number.isFinite(n)))) {
    fail(`--stills must be comma-separated seconds\n  Actual: ${argv.join(' ')}`);
  }
  return out;
}

function loadPlaywright() {
  const mod = process.env.PLAYWRIGHT_MODULE || 'playwright';
  try {
    return require(mod);
  } catch (e) {
    fail(`cannot require playwright\n  Tried: ${mod}\n  Set PLAYWRIGHT_MODULE to an installed node_modules/playwright path\n  Error: ${e.message}`);
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const dir = path.resolve(args.project.replace(/^~/, process.env.HOME));
  const scene = path.join(dir, 'scene.html');
  const tlPath = path.join(dir, 'timeline.json');
  if (!fs.existsSync(scene)) fail(`scene.html not found\n  Path: ${scene}`);
  if (!fs.existsSync(tlPath)) fail(`timeline.json not found (run tts.py first)\n  Path: ${tlPath}`);
  const tl = JSON.parse(fs.readFileSync(tlPath, 'utf8'));

  const { chromium } = loadPlaywright();
  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(e.message));
  await page.goto('file://' + scene);

  const contract = await page.evaluate(() => ({
    setup: typeof window.setup === 'function',
    render: typeof window.render === 'function',
    canvas: !!document.getElementById('c'),
    fonts: window.SCENE_FONTS || [],
  }));
  if (!contract.setup || !contract.render || !contract.canvas) {
    await browser.close();
    fail(`scene contract broken\n  Path: ${scene}\n  Actual: ${JSON.stringify(contract)}\n  Expected: window.setup, window.render, <canvas id="c">\n  Page errors: ${pageErrors.join(' | ')}`);
  }
  await page.evaluate(async ({ tl, fonts }) => {
    for (const f of fonts) await document.fonts.load(f);
    window.setup(tl);
  }, { tl, fonts: contract.fonts });

  const grab = async (t) => {
    const url = await page.evaluate((t) => {
      window.render(t);
      return document.getElementById('c').toDataURL('image/jpeg', 0.95);
    }, t);
    if (pageErrors.length) fail(`scene threw at t=${t}\n  ${pageErrors.join('\n  ')}`);
    return Buffer.from(url.split(',')[1], 'base64');
  };

  if (args.stills) {
    const stillDir = path.join(dir, 'stills');
    fs.mkdirSync(stillDir, { recursive: true });
    for (const t of args.stills) {
      const out = path.join(stillDir, `still_${t.toFixed(1)}.jpg`);
      fs.writeFileSync(out, await grab(t));
      console.log(`[flow_coding_vedio/render] still ${out}`);
    }
    await browser.close();
    return;
  }

  const frames = Math.round(tl.total * args.fps);
  const outPath = path.join(dir, 'video_silent.mp4');
  const started = Date.now();
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(args.fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', outPath],
    { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < frames; i++) {
    const buf = await grab(i / args.fps);
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  const code = await new Promise((r) => ff.on('close', r));
  await browser.close();
  if (code !== 0) fail(`ffmpeg exited ${code}\n  Output: ${outPath}`);
  console.log(`[flow_coding_vedio/render] ${frames} frames in ${((Date.now() - started) / 1000).toFixed(1)}s -> ${outPath}`);
}

main().catch((e) => fail(e && e.stack ? e.stack : String(e)));
