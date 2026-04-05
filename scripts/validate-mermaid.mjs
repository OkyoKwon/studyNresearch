/**
 * Mermaid 다이어그램 문법 검증 스크립트.
 *
 * docs/ 내 모든 .md 파일에서 ```mermaid 블록을 추출하고
 * mermaid.parse()로 실제 파싱하여 문법 오류를 사전에 감지한다.
 *
 * 종료 코드: 0 = 모두 통과, 1 = 파싱 오류 있음
 */
import { readFileSync, readdirSync } from "node:fs";
import { join, relative } from "node:path";

// ── DOM 환경을 먼저 구성한 뒤 mermaid를 로드해야 한다. ──
// mermaid는 dompurify를 정적 import하며, dompurify는 최초 로드 시점에
// globalThis.window 존재 여부로 동작 모드를 결정한다.
// 따라서 window를 설정한 뒤 mermaid를 동적 import해야 한다.
import { JSDOM } from "jsdom";

const dom = new JSDOM("<!DOCTYPE html><html><body></body></html>");
globalThis.window = dom.window;
globalThis.document = dom.window.document;
Object.defineProperty(globalThis, "navigator", {
  value: dom.window.navigator,
  writable: true,
  configurable: true,
});

// DOM 환경 설정 완료 후 mermaid 동적 import
const { default: mermaid } = await import("mermaid");

const DOCS_DIR = join(import.meta.dirname, "..", "docs");
const MERMAID_BLOCK_RE = /```mermaid\n([\s\S]*?)```/g;

mermaid.initialize({ startOnLoad: false, securityLevel: "loose" });

// quadrantChart의 JISON 파서는 Node.js 환경에서 비ASCII 문자(한글 등)를
// 지원하지 않는다 (브라우저에서는 정상 동작). quadrantChart는 regex 기반
// 정적 분석(test_mermaid.py)으로 커버하므로, 파서 검증에서는 제외한다.
const SKIP_DIAGRAM_TYPES = new Set(["quadrantChart"]);

function getDiagramType(code) {
  const firstLine = code.trim().split("\n")[0].trim();
  return firstLine.split(/\s/)[0];
}

function collectMdFiles(dir) {
  const files = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...collectMdFiles(fullPath));
    } else if (entry.name.endsWith(".md")) {
      files.push(fullPath);
    }
  }
  return files;
}

function extractBlocks(filePath) {
  const content = readFileSync(filePath, "utf-8");
  const blocks = [];
  let match;
  while ((match = MERMAID_BLOCK_RE.exec(content)) !== null) {
    const lineNum = content.slice(0, match.index).split("\n").length;
    blocks.push({ code: match[1], line: lineNum });
  }
  return blocks;
}

async function main() {
  const files = collectMdFiles(DOCS_DIR);
  let total = 0;
  let failed = 0;
  const errors = [];

  for (const filePath of files) {
    const blocks = extractBlocks(filePath);
    const relPath = relative(join(DOCS_DIR, ".."), filePath);

    for (const { code, line } of blocks) {
      const trimmed = code.trim();
      const diagramType = getDiagramType(trimmed);

      if (SKIP_DIAGRAM_TYPES.has(diagramType)) {
        continue;
      }

      total++;
      try {
        await mermaid.parse(trimmed);
      } catch (err) {
        failed++;
        const msg = err.message || String(err);
        const shortMsg = msg.split("\n")[0];
        errors.push(`  FAIL ${relPath}:${line} → ${shortMsg}`);
      }
    }
  }

  if (errors.length > 0) {
    console.error(`\nMermaid 파싱 오류 ${failed}/${total}건:\n`);
    errors.forEach((e) => console.error(e));
    console.error("");
    process.exit(1);
  }

  console.log(`Mermaid 검증 통과: ${total}개 다이어그램 모두 정상`);
  process.exit(0);
}

main();
