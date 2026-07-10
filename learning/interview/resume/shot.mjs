// 简历 HTML → PNG 截图脚本（高清，自动隐藏下载/打印按钮）
// 用法：
//   cd learning/interview/resume
//   npm install   # 首次（装 playwright）
//   node shot.mjs
// 依赖系统 Chrome（macOS 标准路径），无需下载 chromium。

import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HTML = resolve(__dirname, 'resume.html');
const OUT_PNG = resolve(__dirname, 'resume.png');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const browser = await chromium.launch({ executablePath: CHROME });
const context = await browser.newContext({
  viewport: { width: 794, height: 1123 },
  deviceScaleFactor: 2,
});
const page = await context.newPage();
await page.goto(pathToFileURL(HTML).href, { waitUntil: 'networkidle' });
await page.addStyleTag({
  content: `
    .actions { display: none !important; }
    body { max-width: none !important; }
  `,
});
await page.waitForSelector('img.photo', { state: 'visible' });
await page.waitForTimeout(300);
await page.screenshot({ path: OUT_PNG, fullPage: true, type: 'png' });
console.log(`✓ ${OUT_PNG}`);
await browser.close();
