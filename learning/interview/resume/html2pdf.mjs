import { chromium } from 'playwright'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const input = resolve(process.argv[2] ?? 'resume.html')
const output = resolve(process.argv[3] ?? 'resume.pdf')

const browser = await chromium.launch()
const page = await browser.newPage()
await page.goto(pathToFileURL(input).href, { waitUntil: 'networkidle' })
await page.emulateMedia({ media: 'print' })
await page.pdf({
  path: output,
  format: 'A4',
  printBackground: true,
  margin: { top: '14mm', right: '14mm', bottom: '14mm', left: '14mm' },
  preferCSSPageSize: true,
})
await browser.close()
console.log(`✓ ${output}`)
