import { chromium } from 'playwright'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const input = resolve(process.argv[2] ?? 'ai-engineer-resume.html')
const output = resolve(process.argv[3] ?? 'ai-engineer-resume.pdf')

const browser = await chromium.launch()
const page = await browser.newPage()
await page.goto(pathToFileURL(input).href, { waitUntil: 'networkidle' })
await page.emulateMedia({ media: 'print' })
await page.pdf({
  path: output,
  format: 'A4',
  printBackground: true,
  // 简历 HTML 已自带 A4 内边距；导出不再额外加白边
  margin: { top: '0', right: '0', bottom: '0', left: '0' },
  preferCSSPageSize: true,
})
await browser.close()
console.log(`✓ ${output}`)
